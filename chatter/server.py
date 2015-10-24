#!/usr/bin/env python
""" Simple server to automate chatter with github """

import yaml
import logging
import flask

config=yaml.load(file('/opt/chatter/config.yaml','r'))
app = flask.Flask(__name__)
logging.basicConfig(filename=config['log_file'], level=logging.INFO)

@app.route('/chatter/')
def index():
    logging.info("Chattering!")
    return "<span style='color red'>I am totally a flask!</span>"
