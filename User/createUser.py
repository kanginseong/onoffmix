from logging import fatal
import os
import pymysql
import json
import datetime
import bcrypt
from flask import request
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


createUser = Namespace(
    name='createUser',
    description='createUser API'
)


@createUser.route('')
class CreateUser(Resource):
    def post(self):

        db = setDB()

        data = request.get_json()
        user_name = data['user_name']
        user_pw = data['user_pw']
        user_mail = data['user_mail']

        # name 체크
        base = db.cursor()
        sql = f'select user_name from User \
                where user_name = "{user_name}";'
        base.execute(sql)
        name = base.fetchall()
        if name:
            base.close()
            return {'name': False}
        else:
            # mail 체크
            base = db.cursor()
            sql = f'select user_mail from User \
                where user_mail = "{user_mail}";'
            base.execute(sql)
            mail = base.fetchall()
            if mail:
                base.close()
                return {'mail': False}

        user_bcrypt = bcrypt.hashpw(user_pw.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        base = db.cursor()
        sql = f'insert into User(user_name, user_pw, user_mail) \
                values("{user_name}", "{user_bcrypt}", "{user_mail}");'
        base.execute(sql)
        db.commit()
        base.close()
        return {'createUser': True}
