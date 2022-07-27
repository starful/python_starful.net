from flask import Flask, render_template, session
from flask import url_for, redirect, request
from flask import Blueprint
from datetime import datetime
from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session

import json
import os
import logging

ss_line = Blueprint('ss_line', __name__, url_prefix='/api/line')
logger = logging.getLogger(__name__)

@ss_line.route("/hello")
def hello():
   return "Hello line"
   
@ss_line.route('/oauth')
def line():
    return "https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=1656851294&redirect_uri=https://www.snkrskin.com/index.html&state=12345abcde&scope=profile%20openid&nonce=09876xyz"
