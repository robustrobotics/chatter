#!/usr/bin/env python
""" Simple server to automate chatter with github """

import yaml
import logging
import flask

#import jenkins_bot

config=yaml.load(file('/opt/chatter/config.yaml','r'))
app = flask.Flask(__name__)
logging.basicConfig(filename=config['log_file'], level=logging.INFO)

@app.route('/chatter/', methods=['GET','POST'])
def chatter():
    if flask.request.method == 'GET':
        logging.info("Chattering! GET")
        return "Success", 200
    elif flask.request.method == 'POST':
        logging.info("Chattering! POST")
        payload = flask.request.get_json()
        event_type = flask.request.headers.get('X-Github-Event')
	issue = payload['issue']['number']
        logging.info("Received a comment on issue number {}".format(issue))
	if 'pull_request' in payload['issue']:
            logging.info("Issue is a pull request")
	logging.info("Comment is {}".format(payload['comment']['body']))
        return "Post acknowledged",204
