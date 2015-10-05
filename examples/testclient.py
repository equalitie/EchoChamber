import json
from flask import Flask, request
import request as req

app = Flask(__name__)

SEND_URL = 'http://localhost:9004/send'

def send_message(message, to):
    response = req.post(SEND_URL, json={"message": message, "to": to})
    data = json.loads(response.text)
    print('Response to send request:\n\tSuccess: {0}\n\tQueue Index: {1}'.format(
        data.success, data.queueIndex))

@app.route('/received', methods=['POST'])
def received():
    print('Got message!')
    print(request.params)
    return 'Thanks!'

@app.route('/')
def unknown():
    return 'What?'

app.run(port=9005)

# Send a message to chamber to get the test started
send_message('Hello, world!', 'myself')
