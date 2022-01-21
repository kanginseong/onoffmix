from logging import fatal
import os
from xml.dom.minidom import Identified
import pymysql
import json
import datetime
import bcrypt
from flask_jwt_extended import *
from flask import request
from flask import jsonify
from flask_restx import Resource, Api, Namespace


def setDB():
    db = pymysql.connect(host='localhost',
                    port=3306,
                    user='root',
                    passwd='root0000',
                    db='onoffmix',
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)
    return db

login = Namespace(
    name='login',
    description='login API'
)

@login.route('')
class Login(Resource):
    def put(self):

        db = setDB()

        data = request.get_json()
        user_name = data['user_name']
        user_pw = data['user_pw']

        base = db.cursor()
        sql = f'select user_no from User\
                where user_name = "{user_name}";'
        base.execute(sql)
        user = base.fetchall()
        base.close()

        base = db.cursor()
        sql = f'select user_name from User\
                where user_name = "{user_name}";'
        base.execute(sql)
        data = base.fetchall()
        base.close()

        if data:
            base = db.cursor()
            sql = f'select user_pw\
                    from User\
                    where user_name = "{user_name}"'
            base.execute(sql)
            pw = base.fetchall()
            for r in pw:
                user_bcrypt = r['user_pw']
                PW = bcrypt.checkpw(user_pw.encode(
                    'utf-8'), user_bcrypt.encode('utf-8'))

                return jsonify(
                    token = "Bearer " + create_access_token( 
                    identity = user,
                    expires_delta = False
					),
                    login = True
                )
        else:
            return {'login' : False}