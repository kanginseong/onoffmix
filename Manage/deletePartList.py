from logging import fatal
import os
import pymysql
import json
import datetime
import bcrypt
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

deletePartList = Namespace(
    name='deletePartList',
    description='deletePartList API'
)

@deletePartList.route('')
class DeletePartList(Resource):
    def delete(self):
        
        user_no = getUser.whoami()

        db = setDB()

        data = request.get_json()
        
        meet_no = data['meet_no']
        form_no = data['form_no']
        
        sql = f'select formuser_no from FormUser where meet_no = {meet_no} and form_no = {form_no} and user_no = {user_no}'

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()

        formuser_no = data[0]['formuser_no']

        sql = f'delete from FormUser where formuser_no = {formuser_no}'

        base = db.cursor()
        base.execute(sql)
        db.commit()
        base.close()

        return {"deletePartList" : True}
        
        
        