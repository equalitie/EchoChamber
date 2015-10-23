import json
import requests
from flask import Flask, request

app = Flask(__name))

my_id = ''
participants = []

success_true = json.dumps({'success': True})

SEND_URL = 'http://localhost:9004/send'

def send_message(message, to):
    json_data = {'message': message, 'to': to}
    response = req.post(SEND_URL, json=json_data)
    data = json.loads(response.text)
    print('Response to send request:\n\tSuccess: {0}\n\tQueue Index: {1}'.format(
        data['success'], data['queueIndex']))


@app.route('/joined', methods=['POST'])
def joined():
    my_id = request.params['id']
    participants = request.params['participants']
    print 'Got POST /joined request. Set ID to {0}'.format(my_id)
    return success_true


@app.route('/received', methods=['POST'])
def received():
    date = request.params['date']
    _from = request.params['from']
    msg = request.params['message']
    print '{0} {1}: {2}'.format(date, _from, msg)
    return success_true


@app.route('/prompt', methods=['POST'])
def prompt():
    to = request.params['to']
    msg = request.params['message']
    print 'Prompted to send to {0}: {1}'.format(to, message)
    send_message(msg, to)
    return success_true


@app.route('/disconnect', methods=['POST'])
def disconnect():
    print 'Told to disconnect'
    sys.exit(1)


app.run(port=9005)
