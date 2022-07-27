from flask import Flask, render_template, session
from flask import url_for, redirect, request
from flask import Blueprint
from datetime import datetime

import os
import logging


upload = Blueprint('upload', __name__, url_prefix='/api/upload')

# __name__はこのモジュールの名前
logger = logging.getLogger(__name__)

@upload.route('/hello2', methods=['GET'])
def hello2():
   return "Hello upload"

@upload.route('/image', methods=['POST'])
def do_upload():
    upload =request.files['data']
    savefilename = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3] + "_" + upload.filename
    print(savefilename)
    if upload is None:
        print("null")
    else:
        print(upload)
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 'File extension not allowed.'
    upload.save("/opt/img/" + savefilename)
    return 'Upload OK. FilePath: %s%s' % ("/opt/img/", savefilename)