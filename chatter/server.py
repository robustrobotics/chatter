#!/usr/bin/env python
""" Simple server to automate chatter with github """

import yaml
import logging
import flask

import jenkins_bot

config=yaml.load(file('/opt/chatter/config.yaml','r'))
app = flask.Flask(__name__)
logging.basicConfig(filename=config['log_file'], level=logging.INFO)

@app.route('/chatter/', methods['GET','POST'])
def chatter():
    logging.info(request)
    if request.method == 'GET':
        logging.info("Chattering! GET")
    elif request.method == 'POST':
        logging.info("Chattering! POST")
    return "Success"
