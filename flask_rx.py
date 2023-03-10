import urllib3
import json
import os
import time
import cryptography
from flask import Flask, request, abort, send_from_directory
from flask_basicauth import BasicAuth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings
from config import WEBHOOK_USERNAME, WEBHOOK_PASSWORD
save_webhook_output_file = "all_webhooks_detailed.json"

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = WEBHOOK_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = WEBHOOK_PASSWORD

# If true, then site wide authentication is needed
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

@app.route('/')  # create a route for / - just to test server is up.
@basic_auth.required
def index():
    return '<h1>Flask Receiver App is Up!</h1>', 200

@app.route('/webhook', methods=['POST'])  # create a route for /webhook, method POST
@basic_auth.required
def webhook():
    if request.method == 'POST':
        print('Webhook Received')
        request_json = request.json

        # print the received notification
        print('Payload: ')
        # Change from original - remove the need for function to print
        print(json.dumps(request_json,indent=4))

        # save as a file, create new file if not existing, append to existing file
        # full details of each notification to file 'all_webhooks_detailed.json'
        # Change above save_webhook_output_file to a different filename

        with open(save_webhook_output_file, 'a') as filehandle:
            # Change from original - we output to file so that the we page works better with the newlines.
            filehandle.write('%s\n' % json.dumps(request_json,indent=4))
            filehandle.write('= - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - \n')

        return 'Webhook notification received', 202
    else:
        return 'POST Method not supported', 405

if __name__ == '__main__':
    # HTTPS enable - toggle on eby un-commenting
    app.run(ssl_context='adhoc', host='0.0.0.0', port=5443, debug=True)
    # HTTP ONLY enable - toggle on eby un-commenting
    # app.run(host='0.0.0.0', port=5443, debug=True)
# Check firewall is not block 5443
# $ sudo ufw allow 5443
# if 'inactive' response means firewall is not on.
# 
# Use the following to see if the port is listen for flask.
# $ sudo lsof -i -P -n | grep LISTEN
#
# Test with - Change IP address first
# $ curl --insecure --user "username:password" --header "Content-Type: application/json" --request POST --data '{"emailAddress":"pnhan@cisco.com"}' https://XX.XX.XX.XX:5443/webhook
# OR
# $ python3 test_webhook.py
