from flask import Flask, render_template, session
from flask import url_for, redirect, request
from flask import Blueprint
from datetime import datetime
from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session

import json
import os
import logging

ga = Blueprint('ga', __name__, url_prefix='/api/ga')
logger = logging.getLogger(__name__)

@ga.route("/hello")
def hello():
   return "Hello ga"

# Sessionの暗号化に使う任意の文字列(適当でOK)
# ga.secret_key = 'A0Zr98j/3yX Rnaxaixaixasdwqazxqe123adcH!jmN]LWX/,?RT'
# GOOGLE_CLIENT_ID = '350108786002-ipeuqj91d6sbcm7d4p8la3j6fpm6hc9d.apps.googleusercontent.com'
# GOOGLE_CLIENT_SECRET = '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'

@ga.route('/oauth')
def google():
  return 'https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A//www.googleapis.com/auth/drive.metadata.readonly'\
  '&include_granted_scopes=true'\
  '&response_type=token'\
  '&state=state_parameter_passthrough_value'\
  '&redirect_uri=https%3A//www.starful.net/index.html'\
  '&client_id=350108786002-ipeuqj91d6sbcm7d4p8la3j6fpm6hc9d.apps.googleusercontent.com'

#     GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
#     GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
#     CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
#     oauth.register(
#         name='google',
#         client_id=GOOGLE_CLIENT_ID,
#         client_secret=GOOGLE_CLIENT_SECRET,
#         server_metadata_url=CONF_URL,
#         client_kwargs={
#             'scope': 'openid email profile'
#         }
#     )
#     # redirect_uri = url_for('google_auth', _external=True)
#     redirect_uri = "https://www.starful.net/api/ga/auth"
#     # print("redirect_uri : " + redirect_uri)
#     # return oauth.google.authorize_redirect(redirect_uri)
#     return "https://www.starful.net/api/ga/auth"

# @ga.route('/auth')
# def google_auth():
#     print("google_auth()")
#     token = oauth.google.authorize_access_token()
#     user = oauth.google.parse_id_token(token)
#     print(" Google User ", user)
#     # return redirect('/')
#     return "https://www.starful.net/index.html"
