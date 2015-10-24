#!/usr/bin/env python
""" Simple server to automate chatter with github """

import os
import logging
import flask

app = flask.Flask(__name__)
logging.basicConfig(filename=os.environ['CHATTER_LOG_FILE'],level=logging.INFO)

@app.route('/chatter/')
def index():
    logging.info("Chattering!")
    return "<span style='color red'>I am totally a flask!</span>"
