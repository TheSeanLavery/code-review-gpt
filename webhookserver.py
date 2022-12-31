from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
  # Get the JSON payload sent by GitHub
  payload = request.get_json()
  
  # Do something with the payload, such as updating an external issue tracker
  # or triggering a CI build
  print(payload)
  return 'Success'

if __name__ == '__main__':
  app.run()

