from flask import Flask, render_template, session
from flask import url_for, redirect, request
from flask import Blueprint
from datetime import datetime
from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session

import json
import os
import logging

tw = Blueprint('tw', __name__, url_prefix='/api/tw')
logger = logging.getLogger(__name__)

@tw.route("/hello")
def hello():
   return "Hello tw"

# トップ画面
@tw.route('/login')
def index():
    # セッションが既にあればアカウントIDを表示、なければログインボタンを表示
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = []
    # return render_template("upload.html", user_name=user_name)
    return redirect("https://www.starful.net/upload.html")

# Twitterの認証画面にリダイレクトする
@tw.route("/oauth")
def twOauth():
    # Twitter Application Management で設定したコールバックURLsのどれか
    oauth_callback = request.args.get('oauth_callback')
    # Twitter認証画面のURLを生成する
    callback = get_twitter_request_token(oauth_callback)
    # 認証画面にリダイレクトする
    return callback

@tw.route('/callback')
def execute_userinfo():
    """[認証画面から返されてきた情報を取得して処理する関数]
    Return [ホーム画面('/')にリダイレクトする]
    """
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    # リクエストトークンからアクセストークンを取得
    access_token = get_twitter_access_token(oauth_token, oauth_verifier)

    # 既に登録していないかチェック、無ければ新規にデータをテーブルにINSERTする
    # 既に登録済みであれば、その情報を返す
    user_data = db.search_user(access_token)
    if user_data is False:
        # 新規ユーザーはアクセストークンの情報をデータベースに保存
        db.register_userinfo(access_token)
        # 登録してからもう一回ユーザーデータを取得
        user_data = db.search_user(access_token)
    # 返された情報をSessionに保存する
    session['user_name'] = access_token['screen_name']
    session['user_id'] = access_token['user_id']
    session['oauth_token'] = access_token['oauth_token']
    session['oauth_token_secret'] = access_token['oauth_token_secret']
    # トップ画面にリダイレクトする
    return redirect("https://www.starful.net/index.html")

@tw.route("/logout")
def logout():
    # セッションに渡しているデータを削除
    session.pop('user_name', None)
    session.pop('user_id', None)
    session.pop('oauth_token', None)
    session.pop('oauth_secret', None)
    return "https://www.starful.net/login.html"


##############################################################################################################
# ここに自分のAPI鍵を入力してください
consumer_key = 'TuK2T7V1mGiET7TcfbXD05g6C'
consumer_secret = 'w26lB9ABwnWV8lY9ZhikaT7FCniauENhWrzdjqtUyWHVzzjUou'
access_key = '1481863414632706048-8yXLPvrZKsjAU8A22p46ZPmpMnG1dW'
access_secret = 'EpBUElXmwW3SQ6ymTVlEJAWTjx8xAZs8NequxSVhINxOY'

# base urls for oauth
base_url = 'https://api.twitter.com/'
request_token_url = base_url + 'oauth/request_token'
authenticate_url = base_url + 'oauth/authenticate'
access_token_url = base_url + 'oauth/access_token'
base_json_url = 'https://api.twitter.com/1.1/%s.json'
user_timeline_url = base_json_url % ('statuses/user_timeline')

def get_twitter_request_token(oauth_callback):
    twitter = OAuth1Session(consumer_key, consumer_secret)
    response = twitter.post(request_token_url, params={'oauth_callback': oauth_callback})
    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    # リクエストトークンから認証画面のURLを生成
    authenticate_endpoint = '%s?oauth_token=%s' \
        % (authenticate_url, request_token['oauth_token'])

    request_token.update({'authenticate_endpoint': authenticate_endpoint})
    return request_token['authenticate_endpoint']


def get_twitter_access_token(oauth_token, oauth_verifier):
    # twitterのデータベース？にアクセスする準備
    twitter = OAuth1Session(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_verifier,
        )

    # ユーザーの返してきたアクセストークンと自分のAPI鍵セットした状態でツイッターに殴り込みをかける
    response = twitter.post(access_token_url, params={'oauth_verifier': oauth_verifier})

    # レスポンスの中にアクセストークンを取得する(これがお目当てのもの)
    access_token = dict(parse_qsl(response.content.decode("utf-8")))
    return access_token    