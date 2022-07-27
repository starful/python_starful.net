from flask import Flask, render_template, session, jsonify, json
from flask import url_for, redirect, request
from flask import Blueprint

import sys
import os
import logging
import sqlite3
import json
from datetime import datetime

mbti = Blueprint('mbti', __name__, url_prefix='/api/mbti')
logger = logging.getLogger(__name__)
db_path = "/opt/db/mbti.db"

@mbti.route("/hello")
def hello():
   return "Hello mbti"


# USERT Register
@mbti.route('/userRegister', methods=['POST','OPTIONS'])
def userRegister():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    certification = '0'
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # INSERT INTO `accounts` (`Username`, `Password`, `Email`, 'Certification') VALUES ('test3', 'test3', 'test3@test.com', '0');
    result = commit_query_db(db_path, 'insert into "ACCOUNTS" (`Username`, `Password`, `Email`, `Certification`, "Reg_datetime", "Update_datetime") \
        values (?, ?, ?, ?, ?, ?)',(str(username),str(password),str(email),str(certification),str(current_date),str(current_date),))
    return str(result)

# BBS LIST SELECT
@mbti.route('/userLogin', methods=['POST','OPTIONS'])
def userLogin():
    username = request.json['username']
    password = request.json['password']
    
    datas = query_db(db_path, 'select count(*) as Count from ACCOUNTS where Username = ? and Password = ?',(str(username),str(password),))

    result = {'datas': []}
    result_title = result['datas']

    for c in datas:
        result_title.append({
            "count": c.get('Count')
        })
    print(result)
    return result

# CALCULATION MBTI
@mbti.route('/mbti', methods=['POST','OPTIONS'])
def search():
    result = request.json['result']
    personality_dichotomy: str = ''

    if result.count('A', 0, 5) > result.count('B', 0, 5):
        personality_dichotomy = personality_dichotomy + 'E'
    else:
        personality_dichotomy = personality_dichotomy + 'I'

    if result.count('A', 0, 10) > result.count('B', 0, 10):
        personality_dichotomy = personality_dichotomy + 'S'
    else:
        personality_dichotomy = personality_dichotomy + 'N'

    if result.count('A', 0, 15) > result.count('B', 0, 15):
        personality_dichotomy = personality_dichotomy + 'T'
    else:
        personality_dichotomy = personality_dichotomy + 'F'

    if result.count('A', 0, 20) > result.count('B', 0, 20):
        personality_dichotomy = personality_dichotomy + 'J'
    else:
        personality_dichotomy = personality_dichotomy + 'P'

    data = {'data': personality_dichotomy}
    return jsonify(data)

# BBS LIST SELECT
@mbti.route('/getList', methods=['POST','OPTIONS'])
def getList():
    keyword = request.json['kind']
    print(keyword)
    datas = query_db(db_path, 'select * from BBS where Del_flag = 0 and Kind = ? ORDER BY Reg_datetime desc',(str(keyword),))

    result = {'datas': []}
    result_title = result['datas']

    for d in datas:
        result_title.append({
            "id": d.get('Id'),
            "title": d.get('Title'),
            "kind": d.get('Kind'),
            "contents": d.get('Contents'),
            "reg_user": d.get('Reg_user'),
            "reg_datetime": d.get('Reg_datetime'),
            "update_datetime": d.get('Update_datetime')
        })
    print(result)
    return result

# BBS DETAIL SELECT
@mbti.route('/getDetail', methods=['POST','OPTIONS'])
def getDetail():
    kind = request.json['kind']
    id = request.json['id']

    result = {'datas': [], 'comments': [], 'count': []}

    # SELECT BBS COMMENTS COUNT
    comments_count_result = query_db(db_path, 'select count(*) as Count  from BBS_COMMENTS where Del_flag = 0 and BBSId = ?',(str(id),))
    comments_count = result['count']
    for c in comments_count_result:
        comments_count.append({
            "count": c.get('Count')
        })

    # SELECT BBS COMMENTS
    comments_result = query_db(db_path, 'select * from BBS_COMMENTS where Del_flag = 0 and BBSId = ? ORDER BY Reg_datetime desc',(str(id),))
    comments_bbs = result['comments']
    for c in comments_result:
        comments_bbs.append({
            "id": c.get('Id'),
            "bbsid": c.get('BBSId'),
            "kind": c.get('Kind'),
            "comments": c.get('Comments'),
            "reg_user": c.get('Reg_user'),
            "reg_datetime": c.get('Reg_datetime'),
            "update_datetime": c.get('Update_datetime')
        })

    # SELECT BBS
    datas = query_db(db_path, 'select * from BBS where Del_flag = 0 and Kind = ? and Id = ?',(str(kind),str(id),))
    result_bbs = result['datas']

    for d in datas:
        result_bbs.append({
            "id": d.get('Id'),
            "title": d.get('Title'),
            "kind": d.get('Kind'),
            "contents": d.get('Contents'),
            "reg_user": d.get('Reg_user'),
            "reg_datetime": d.get('Reg_datetime'),
            "update_datetime": d.get('Update_datetime')
        })
    print(result)
    return result

# BBS INSERT
@mbti.route('/insert', methods=['POST','OPTIONS'])
def insert():
    title = request.json['title']
    contents = request.json['contents']
    kind = request.json['kind']
    user = request.json['user']
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = commit_query_db(db_path, 'insert into "BBS" ("Title", "Contents", "Kind", "Reg_user", "Del_flag", "Reg_datetime", "Update_datetime") \
        values (?, ?, ?, ?, 0, ?, ?)',(str(title),str(contents),str(kind),str(user),str(current_date),str(current_date),))
    return str(result)

# BBS UPDATE
@mbti.route('/setDetail', methods=['POST','OPTIONS'])
def setDetail():
    title = request.json['title']
    contents = request.json['contents']
    kind = request.json['kind']
    bbsId = request.json['id']
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = commit_query_db(db_path, 'update BBS SET Title = ?, Contents = ?, Update_datetime = ? WHERE Id = ? AND Kind = ?' \
        ,(str(title),str(contents),str(current_date),str(bbsId),str(kind),))
    return str(result)

# BBS DELETE
@mbti.route('/setDelete', methods=['POST','OPTIONS'])
def setDelete():
    bbsId = request.json['id']
    result = commit_query_db(db_path, 'update BBS SET Del_flag = 1 WHERE Id = ?',(str(bbsId),))
    return str(result)  


# BBS COMMENT INSERT
@mbti.route('/insertComment', methods=['POST','OPTIONS'])
def insertComment():
    bbsId = request.json['id']
    Kind = request.json['kind']
    comment = request.json['comment']
    reg_user = request.json['user']
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = commit_query_db(db_path, 'insert into "BBS_COMMENTS" ("BBSId", "Kind", "Comments", "Reg_user", "Del_flag", "Reg_datetime", "Update_datetime") \
        values (?, ?, ?, ?, 0, ?, ?)',(str(bbsId),str(Kind),str(comment),str(reg_user),str(current_date),str(current_date),))
    return str(result)


# BBS COMMENT UPDATE
@mbti.route('/updateComment', methods=['POST','OPTIONS'])
def updateComment():
    bbsId = request.json['id']
    comment = request.json['comment']
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = commit_query_db(db_path, 'update BBS_COMMENTS SET Comments = ?, Update_datetime = ? WHERE Id = ? ' \
        ,(str(comment),str(current_date),str(bbsId),))
    return str(result)

# BBS COMMENT DELETE
@mbti.route('/deleteComment', methods=['POST','OPTIONS'])
def deleteComment():
    bbsId = request.json['id']
    result = commit_query_db(db_path, 'update BBS_COMMENTS SET Del_flag = 1 WHERE Id = ?',(str(bbsId),))
    return str(result)


# SELECT SQL
def query_db(db_path, query, args=(), one=False):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        print(query)
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
    except sqlite3.Error as e:
        print('query_db : sqlite3.Error occurred:' + str(e.args[0]))
    return (r[0] if r else None) if one else r

# INSERT,UPDATE,DELETE SQL
def commit_query_db(db_path, query, args=(), one=False):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        print(query)
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        conn.commit()
        result = cur.lastrowid
        cur.connection.close()
    except sqlite3.Error as e:
        print('query_db : sqlite3.Error occurred:' + str(e.args[0]))
    return result