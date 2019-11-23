# simple-webservice
A simple web service that listens for organization events to know when a repository has been created. When the repository is created this web service automates the protection of the master branch. It also notifies you with an @mention in an issue within the repository that outlines the protections that were added.

## Usage
- Install the following:
   - [Python](https://www.python.org/downloads/)
   - [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#installation)
   - [ngrok](https://dashboard.ngrok.com/get-started)
- Start the local web service via 'flask run --host=0.0.0.0'
- Start the forwarding service via './ngrok http 5000'
- Note the forwarding address (ie. https://cfe6d829.ngrok.io in the output of the ngrok application
- Set up a WebHook in the desired GitHub organization (ie. https://github.com/buzzmoto-org/REPO/settings/hooks)
   - Note that the Payload URL should match the forwarding address from ngrok (https://blahblah.ngrok.io)
   - Select the individual events radio button and check repositories
   - Save the Webhook

## Related Documentation
- [GitHub APIv3](https://developer.github.com/v3/)
- [Web Hooks](https://developer.github.com/webhooks/)
- [API Status](https://www.githubstatus.com/)
- [Flask Docs](https://flask.palletsprojects.com/en/1.1.x/)
- [ngrok](https://ngrok.com/docs)

## Dependencies and Attribution
- Python
- Flask
- ngrok

## Bugs and corner cases
Note: Payloads are capped at 25 MB. If your event generates a larger payload, a webhook will not be fired. This may happen, for example, on a create event if many branches or tags are pushed at once. We suggest monitoring your payload size to ensure delivery. See [webhooks docs](https://developer.github.com/webhooks/)

## Notes
This could be done with AWS Lambda and an API Gateway once my AWS account stops crashing.
