
from logging import fatal
import os
import pymysql
import json
import datetime
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

# sql = f'insert into User values(${user_name}, ${user_mail}, ${user_pw});'

# print(sql)

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
        user_mail = data['user_mail']
        user_pw = data['user_pw']

        # id 체크
        base = db.cursor()
        sql = f'select user_name from User\
                where user_name = "{user_name}";'
        base.execute(sql)
        id = base.fetchall()
        print(id)
        if id:
            base.close()
            return {'id': False}
        else:
            # mail 체크
            base = db.cursor()
            sql = f'select user_mail from User\
                where user_mail = "{user_mail}";'
            base.execute(sql)
            mail = base.fetchall()
            if mail:
                base.close()
                return {'mail': False}

        
        base = db.cursor()
        sql = f'insert into User(user_name, user_mail, user_pw)\
                values("{user_name}", "{user_mail}", "{user_pw}");'
        base.execute(sql)
        db.commit()
        base.close()
        return {'createUser': True}

    