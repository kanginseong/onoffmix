from logging import fatal
import os
import pymysql
import json
import datetime
from flask import request
from flask_restx import Resource, Api, Namespace

import getUser


def setDB():
    db = pymysql.connect(host='localhost',
                    port=3306,
                    user='root',
                    passwd='root0000',
                    db='onoffmix',
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)
    return db

updateRegiList = Namespace(
    name='updateRegiList',
    description='updateRegiList API'
)

# 방장
@updateRegiList.route('')
class UpdateRegiList(Resource):

    def put(self):

        user_no = getUser.whoami()

        db = setDB()
        
        data = request.get_json()

        meet_no = data['meet_no']
        form_no = data['form_no']
        user2_no = data['user_no'] # 바꿀 사용자
        formuser_state = data['formuser_state']

        sql = f'select user_static from FormUser \
                where meet_no = {meet_no} \
                and form_no = {form_no} \
                and user_no = {user_no} ;'

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()

        sql = f'update FormUser \
                set formuser_state = "{formuser_state} "\
                where user_no = {user2_no};'

        base = db.cursor()
        base.execute(sql)
        db.commit()
        base.close()

        return { "updatePartList" : True }