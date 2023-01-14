from flask import Flask, request

import issues_responder
import PR_review

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
  # Get the JSON payload sent by GitHub
  payload = request.get_json()


  
  pull_request = payload.get('pull_request', None)
  issue = payload.get('issue', None)

  #check if this a pull request or an issue
  if issue != None:
    #get the issue number
    issue_number = payload['issue']['number']
    #get the issue title
    issue_title = payload['issue']['title']
    #get the issue body
    issue_body = payload['issue']['body']
    #get the issue url
    issue_url = payload['issue']['html_url']
    #get the issue state
    issue_state = payload['issue']['state']
    #get the issue user
    issue_user = payload['issue']['user']['login']
    #get the issue user avatar
    issue_user_avatar = payload['issue']['user']['avatar_url']
    issues_responder.respond_to_issue(issue_number)


  if pull_request != None:
    #get the pull request number
    pull_request_number = payload['pull_request']['number']
    #get the pull request title
    pull_request_title = payload['pull_request']['title']
    #get the pull request body
    pull_request_body = payload['pull_request']['body']
    #get the pull request url
    pull_request_url = payload['pull_request']['html_url']
    #get the pull request state
    pull_request_state = payload['pull_request']['state']
    #get the pull request user
    pull_request_user = payload['pull_request']['user']['login']
    #get the pull request user avatar
    pull_request_user_avatar = payload['pull_request']['user']['avatar_url']
    
    PR_review.ReviewPR(pull_request_number)





  # Do something with the payload, such as updating an external issue tracker
  # or triggering a CI build
  print(payload)

  #add the payload to a log file, create a new log file if it doesn't exist
  with open('log.txt', 'a') as f:
    f.write(str(payload))
    f.write('\n')
  

  # Return a 200 OK response to let GitHub know the webhook was received
  # successfully
  return '', 200


#delete the logfile route
@app.route('/webhookdelete', methods=['GET'])
def webhook_delete():
  #delete the log file
  with open('log.txt', 'w') as f:
    f.write('')
  return 'Log file deleted'

@app.route('/webhookget', methods=['GET'])
def webhook_get():
  #serve the log file
  with open('log.txt', 'r') as f:
    log = f.read()
  return log

if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=8080)
  print("Server started on port 8080")  

