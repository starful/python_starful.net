from flask import Flask, render_template, session
from flask import url_for, redirect, request
from flask import Blueprint
import email
import smtplib
import logging

mail = Blueprint('mail', __name__, url_prefix='/api/mail')

# __name__はこのモジュールの名前
logger = logging.getLogger(__name__)

# メールアドレス :   starful@starful.net
# アカウント(ユーザー名) :  starful@starful.net
# パスワード : 7278hwan##

# SMTPサーバー :  smtp22.gmoserver.jp
# POPサーバー :   pop22.gmoserver.jp
# https://www.starful.net/api/mail/send2
@mail.route('/send2', methods=['GET'])
def send2():
    return 'Hello send2'

# https://www.starful.net/api/mail/send?title=title&email=email@email.com&sub=subsubsubsubsubsubsubsubsubsubsubsubsubsubsubsubsubsub
@mail.route('/send', methods=['GET'])
def email_send():

    print(request.args.get('title'))
    print(request.args.get('email'))
    print(request.args.get('sub'))

    logger.debug("test")

    email_to = 'starful@starful.net'
    # fromMy  = 'starful@starful.net'
    email_from  = request.args.get('email')
    subj = request.args.get('title')
    message = request.args.get('sub')

    # msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % ( fromMy, to, subj, message_text )

    username = str('starful@starful.net')
    password = str('7278hwan##')

    try:
        server = smtplib.SMTP("smtp22.gmoserver.jp",587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username,password)
        server.sendmail(email_from, email_to, message)
        server.quit()
        return 'ok the email has sent'
    except Exception as e:
        return str("NG : " + e)