import json
import os  # pylint: disable=import-error
import time  # pylint: disable=import-error

import requests  # pylint: disable=import-error
print('Loading function')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    payload = json.loads(json.dumps(event))
    body_str = payload["body"]
    print("body_str",body_str  )
    payload = json.loads(body_str)
    print(payload)
    
    user = "learnazcloud"
    cred = "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"
	
	
    if payload is None:
        print("POST was not formatted in JSON")

    # Verify the repo was created
    try:
        if payload["action"] == "created" or payload["action"] == "publicized":
            # Delay needed for server to be create the page, otherwise a 404 returns
            time.sleep(1)
            # Create branch protection for the master branch of the repo
            branch_protection = {
                "required_status_checks": {"strict": True, "contexts": ["default"]},
                "enforce_admins": False,
                "required_pull_request_reviews": None,
                "restrictions": None,
            }
            session = requests.session()
            session.auth = (user, cred)
            response_1 = session.put(
                payload["repository"]["url"] + "/branches/main/protection",
                json.dumps(branch_protection),
            )
            if response_1.status_code == 200:
                print(
                    "AuthTest: Branch protection created successfully. Status code: ",
                    response_1.status_code,
                )

                # Create issue in repo notifying user of branch protection
                try:
                    if payload["repository"]["has_issues"]:
                        issue = {
                            "title": "AuthTest: New Protection Added",
                            "body": "AuthTest: @"
                            + user
                            + " @learnazcloud-secteam A new branch protection was added to the master branch.",
                        }
                        session = requests.session()
                        session.auth = (user, cred)
                        response_2 = session.post(
                            payload["repository"]["url"] + "/issues", json.dumps(issue)
                        )
                        if response_2.status_code == 201:
                            print(
                                "AuthTest: Issue created successfully. Status code: ",
                                response_2.status_code,
                            )
                        else:
                            print(
                                "AuthTest: Unable to create issue. Status code: ",
                                response_2.status_code,
                            )
                    else:
                        print(
                            "AuthTest: This repo has no issues so one cannot be created at this time."
                        )
                except KeyError:
                    # Request did not contain information about if the repository has issues enabled
                    pass
            else:
                print(response_1.content)
                print(
                    "AuthTest: Unable to create branch protection. Status code: ",
                    response_1.status_code,
                )
    except KeyError:
        # Ignore POST payload since it is not a create action
        pass

    return "AuthTest: OK"
   
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(payload),
    }
