# Auto Branch Protect
Forked from Zack Koppert's Auto Branch Protect Tool for GitHub's Technical Assessment
credits - https://www.codefactor.io/repository/github/zkoppert/auto-branch-protect

Auto branch protect is a simple web service that listens for organization events to know when a repository has been created. When the repository is created this web service automates the protection of the main branch. It also notifies you with an @mention in an issue within the repository that outlines the protections that were added.

## Usage
- Install the following:
  - [Python](https://www.python.org/downloads/)
    - `pip install -r requirements.txt`
  - [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#installation)
  - [ngrok](https://dashboard.ngrok.com/get-started)

- Next step is to browse to a file path of your choice on your local machine & run following command (in command prompt) to clone this repository on your local machine
        git clone https://github.com/learnazcloud/Auto-branch-protect.git

There are three main parts to this tool. 
1. app.py - This  is a python script which receives payload from GitHub via webhook and processes the information. The script identifies that a new repository is created and adds a branch protection rule to the main branch. A new issue is created notifying the user defined in the script. 
    a. The script needs GitHub token for the administrator user to run this script. 
    b. In this scenario the user is @learnazcloud
    c. The token is obtained from User --> Settings --> Developer Settings --> Personal Access Tokens --> Generate New Token
    d. The token from here is then set as an environment variable by using following command in "Command Prompt" on windows. 
       set GH_TOKEN = abcd_1223458605  (ofcourse that's not a real token!!)
    e. Remember to set the GH_TOKEN if a new command prompt window is opened for invoking another instance. Otherwise it throws "KeyError" : 'GH_TOKEN' error. 
2. Flask - This creates a local web service by running app.py at http://localhost:5000
    a. Following commands were run in command prompt to prepare flask
       set FLASK_ENV=development
       set FLASK_APP=app.py
       flask run
    b. This will start the flask on your local machine at http://localhost:5000. The ip address for localhost may differ.
3. Ngrok - This is used to expose the Flask app running at http://localhost:5000 to external facing service. Once setup Ngrok provides a forward URL which is used as a webhook in the following steps. 
    a. You need to first signup at http://ngrok.com. You can use your GitHub account to sign up.
    b. Next step is to download ngrok on your local machine. For windows, it provides ngrok.exe. You need to copy it to the folder location where you had cloned the repository. 
    c. Next step is to get AuthToken. This is available when you logon to ngrok.com under getting started --> Your AuthToken
    d. Open a new command prompt and type following command to set ngrok authtoken env variable on your machine
            ngrok authtoken 25wTBihXXXXXXXXXXXXXX
    e. Once this is set, type following command to expose flask app with ngrok
            ngrok http http://localhost:5000 -host-header="localhost:5000"
    f. This provides a http and https forwarding urls as an output
    g. Copy the http forwarding URL to use as a webhook in GitHub
4. Setting up Webhook in GitHub
    a. Login to GitHub as the user which was used to create an "Organization" in GitHub. In this case, @learnazcloud
    b. Click on the right hand corner on the user profile and select "Your Organizations"
    c. Select the organization and go to settings
    d. Select "webhooks" from the left side menu
    e. Click "Create a new webhook"
        i.    For "Payload URL" - Use the http forwarding URL from the ngrok setup.
        ii.   Content type - application/json 
        iii.  secret - leave blank
        iv. Which events would you like to trigger this webhook?
              - select "let me select individual events".
              - select "Repositories". Unselect "Pushes"
        v. Click "Add Webhook"
5. Test the scenario
    a. Create two dummy users for testing. In this scenario I created @learnazcloud-user00 and @learnazcloud-user01. 
    b. Login as @learnazcloud and add the dummy users to organization as members
    c. Login as @learnazcloud-user00 and create a new repository with README.MD file (This enforces a new branch creation)
    d. GitHub EventType API generates a response to this event and sends it to the webhook that was setup earlier.
    e. The payload is then passed by ngrok via the forwarding url to flask app on localhost:5000.
    f. The post method inside the python script receives the payload and performs the actions to add branch protection rules and issues with notification
    g. Login as @learnazcloud-secteam to confirm the notifications. 
    h. login as @learnazcloud-user01 to perform a commit and validate that the user is prevented from merging
    i. Login as @learnazcloud-user00 to validate that the user can perform the reviews and merge operations.     
 
## Alternate architecture with AWS Lambda and Amazon API Gateway
1. AWS Lambda script is included in the repository under "aws_lambda" folder. 
2. Logon to AWS console and create a new lambda function. Paste the function code from the "lambda_function.py" file from "aws_lambda" folder
3. Add python39.zip as layer since AWS Lambda doesn't have all the needed python libraries.
4. Also add AWS standard layer for python39 which takes care of any missing libraries.  
5. Click on Add Trigger. Select API_Gatway. Select "Create API". Select HTTP API. Select "Auto Deploy"
6. Copy the invoke_url and add route if there is any created. This URL is used as a webhook
7. Follow instructions from "setting up webhook in Github" and complete the setup
8. Test the scenario from the previous instructions 
 
## Modifications from Zack's original code
1. Added A security Team User @learnazcloud-secteam
  a. This repo is forked from Zack's original repository => https://github.com/zkoppert/Auto-branch-protect and following updates were made
  b. In Zack's original code, he used the user who owned the organization for notifications. However, it was observed that the administrator user didn't receive an email or web notification. In my scenario this user is "@learnazcloud". 
  c. Changing "Notification Settings" for the owner user (learnazcloud) to enable "include your own updates" option under "Email notification preferences".
  This sent an email alert however the web notification was still not coming through. This behaviour is by functionality. 
  d. To solve it a new user "learnazcloud-secteam" was created and added to the organization members. The script was updated to include a mention to this user which sent both email and web notifications to this new user. Thus mimicking a true scenario of the security team being notified in case of new repository creations. 
  e. If you would like to change this to anyother user then please go to line 73 of app.py & change the user instead of @learnazcloud-secteam
      + " @learnazcloud-secteam A new branch protection was added to the master branch.",
  
 2. Zack's original code added branch protection only when new repository is "Public". When a new repository is private, the branch protection can only be added with a "Pro" Plan. When with a free plan, if a visibility of a private repository, is changed to "public", then the protection rules were not added.
    a. To fix this payload["action"] == "publicized" was added to line no 24 of app.py
    b. This identifies an event of changing the visibility of a repository from "Private" to "Public"
    
 3. Branch Protection Rules were expanded to following => https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads
      branch_protection = {
				"required_status_checks": None,
				"pull_request_reviews_enforcement_level": "off",
				"required_approving_review_count": 1,
				"dismiss_stale_reviews_on_push": True,
				"require_code_owner_review": True,
				"authorized_dismissal_actors_only": False,
				"ignore_approvals_from_contributors": False,
				"required_status_checks_enforcement_level": "non_admins",
				"strict_required_status_checks_policy": False,
				"signature_requirement_enforcement_level": "off",
				"linear_history_requirement_enforcement_level": "off",
				"enforce_admins": False,
				"allow_force_pushes_enforcement_level": "off",
				"allow_deletions_enforcement_level": "off",
				"merge_queue_enforcement_level": "off",
				"required_deployments_enforcement_level": "off",
				"required_conversation_resolution_level": "off",
				"authorized_actors_only": True,
				"authorized_actor_names": [
				  "learnazcloud-user00"
				],
				"required_pull_request_reviews": None,
                "restrictions": None,
            }
  However the code still needs extended testing to test each settings. 
  4. Zack's original code refers to "master" as the default branch. However, I used "main" as the default branch in my organization. Therefore, the script threw errors that the branch was not found. This can be fixed in two ways - 
      a. Go to the organization --> settings --> Branches & change the default branch to "master" instead of "main"
      --OR --
      b. Go to app.py on line 53 and under "/branches/master/protection" change it to "/branches/main/protection". 
             payload["repository"]["url"] + "/branches/main/protection",

## Related Documentation from Zack's README
- [GitHub APIv3](https://developer.github.com/v3/)
- [Web Hooks](https://developer.github.com/webhooks/)
- [API Status](https://www.githubstatus.com/)
- [Flask Docs](https://flask.palletsprojects.com/en/1.1.x/)
- [ngrok](https://ngrok.com/docs)

## Dependencies and Attribution
- Python
- Flask
- ngrok

## Bugs and improvements
- Payloads are capped at 25 MB. If your event generates a larger payload, a webhook will not be fired. This may happen, for example, on a create event if many branches or tags are pushed at once. We suggest monitoring your payload size to ensure delivery. See [webhooks docs](https://developer.github.com/webhooks/)
- There is a 1 second Delay built in to the code which is NOT ideal. It seems the code is checking for the main branch before it is finished creating.
