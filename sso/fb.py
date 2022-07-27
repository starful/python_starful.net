from flask import Flask, render_template, session
from flask import url_for, redirect, request
from flask import Blueprint
from datetime import datetime
from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session

import json
import os
import logging

fb = Blueprint('fb', __name__, url_prefix='/api/fb')
logger = logging.getLogger(__name__)

@fb.route("/hello")
def hello():
   return "Hello fb"

@fb.route("/oauth")
def fbOauth():
    return 'https://www.facebook.com/v12.0/dialog/oauth?client_id=229166156048113&redirect_uri=https://www.starful.net/index.html'