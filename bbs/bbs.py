from flask import Flask, render_template, session
from flask import url_for, redirect, request
from flask import Blueprint
from datetime import datetime

import sqlite3
import json
import email
import smtplib
import logging
import os
import sys

bbs = Blueprint('bbs', __name__, url_prefix='/api/bbs')
logger = logging.getLogger(__name__)

@bbs.route("/hello")
def hello():
   return "Hello bbs"

@bbs.route('/search', methods=['GET'])
def search():
    datas = []
    keyword = request.args.get('keyword')
    print(keyword)
    datas = query_db("/opt/db/info.db", 'select * from human where name LIKE ?',('%{}%'.format(str(keyword)),))

    result = {'datas': []}
    result_title = result['datas']

    for d in datas:
        result_title.append({
            "id": d.get('id'),
            "name": d.get('name'),
            "part": d.get('part'),
            "position": d.get('position'),
            "mail": d.get('mail'),
            "etc": d.get('etc')
        })
    print(result)
    return result

@bbs.route('/searchId', methods=['GET'])
def searchId():
    datas = []
    keyword = request.args.get('keyword')
    print(keyword)
    datas = query_db("/opt/db/info.db", 'select * from human where id = ?',(str(keyword),))

    result = {'datas': []}
    result_title = result['datas']

    for d in datas:
        result_title.append({
            "id": d.get('id'),
            "name": d.get('name'),
            "part": d.get('part'),
            "position": d.get('position'),
            "mail": d.get('mail'),
            "etc": d.get('etc')
        })

    return result

@bbs.route('/comment', methods=['GET'])
def searchComment():
    datas = []
    keyword = request.args.get('keyword')
    print(keyword)
    datas = query_db("/opt/db/info.db", 'select * from human as a, human_comment as b where a.id = b.human_id and a.id = ?',(keyword,))
    datas_avg = query_db("/opt/db/info.db", 'select AVG(c.eva_a)as eva_a, AVG(c.eva_b)as eva_b, AVG(c.eva_c)as eva_c, AVG(c.eva_d)as eva_d, AVG(c.eva_e)as eva_e from human as a, human_evaluation as c where a.id = c.human_id  and a.id = ?',(keyword,))

    result = {'datas': [], 'datas_avg':[]}

    result_comment = result['datas']
    for d in datas:
        result_comment.append({
            "id": d.get('id'),
            "name": d.get('name'),
            "part": d.get('part'),
            "position": d.get('position'),
            "mail": d.get('mail'),
            "etc": d.get('etc'),
            "text": d.get('text'),
            "reg_time": d.get('reg_time')
        })

    result_eva_avg = result['datas_avg']
    for d in datas_avg:
        result_eva_avg.append({
            "eva_a": d.get('eva_a'),
            "eva_b": d.get('eva_b'),
            "eva_c": d.get('eva_c'),
            "eva_d": d.get('eva_d'),
            "eva_e": d.get('eva_e')
        })

    return result

def query_db(db_path, query, args=(), one=False):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
    except sqlite3.Error as e:
        print('query_db : sqlite3.Error occurred:' + str(e.args[0]))
    return (r[0] if r else None) if one else r
