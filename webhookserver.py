from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
  # Get the JSON payload sent by GitHub
  payload = request.get_json()
  
  # Do something with the payload, such as updating an external issue tracker
  # or triggering a CI build
  print(payload)

  #add the payload to a log file, create a new log file if it doesn't exist
  with open('log.txt', 'a') as f:
    f.write(str(payload))
    f.write(' ')
  
  # Return a 200 OK response to let GitHub know the webhook was received
  # successfully
  return '', 200


@app.route('/webhook', methods=['GET'])
def webhook_get():
  #serve the log file
  with open('log.txt', 'r') as f:
    log = f.read()
  return log

if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=8080)
  print("Server started on port 8080")  

