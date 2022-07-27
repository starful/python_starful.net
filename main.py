from flask import Flask, render_template, session, jsonify
from flask import url_for, redirect, request
from flask_cors import CORS, cross_origin
from authlib.integrations.flask_client import OAuth

from mail.email import mail
from upload.upload import upload
from sso.tw import tw
from sso.fb import fb
from sso.line import ss_line
from sso.ga import ga
from sel.gasearch import gasearch
from bbs.bbs import bbs
from mbti.mbti import mbti

app = Flask(__name__)
CORS(app)
oauth = OAuth(app)

app.register_blueprint(mail)
app.register_blueprint(upload)
app.register_blueprint(tw)
app.register_blueprint(fb)
app.register_blueprint(ss_line)
app.register_blueprint(ga)
app.register_blueprint(gasearch)
app.register_blueprint(bbs)
app.register_blueprint(mbti)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Methods', '*')
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')

  return response

@app.route('/api/hello')
def index():
    return 'Hello main'

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=90, debug=True)