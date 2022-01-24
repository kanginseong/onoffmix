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

updateMeet = Namespace(
    name='createMeet',
    description='createMeet API'
)

@updateMeet.route('')
class UpdateMeet(Resource):
    def put(self):
        
        user_no = getUser.whoami()

        db = setDB()

        data = request.get_json()
        meet_no = data['meet_no']
        meet_title = data['meet_title']
        meet_content = data['meet_content']
        
        sql = f'select meet_no from Meet\
                where user_no = {user_no} and meet_no = {meet_no};'
        base = db.cursor()
        base.execute(sql)
        check = base.fetchall()
        base.close()

        # 내가 만든 방이면 수정가능
        if check:
            sql = f'update Meet set meet_title = "{meet_title}", meet_content = "{meet_content}"\
                    where user_no = {user_no} and meet_no = {meet_no};'
            base = db.cursor()
            base.execute(sql)
            db.commit()
            base.close()

            sql = f'select form_no from Form \
                    where meet_no = {meet_no};'
            base = db.cursor()
            base.execute(sql)
            form = base.fetchall()
            base.close()
            
            group = data['group']

            if len(group) == len(form):

                for i, j in zip(group, form):  
                    sqll = f'update Form set\
                            form_title = "{i["form_title"]}", \
                            form_total = {i["form_total"]}, \
                            form_admission = "{i["form_admission"]}", \
                            form_meet_start = "{i["form_meet_start"]}", \
                            form_meet_end = "{i["form_meet_end"]}", \
                            form_apply_start =  "{i["form_apply_start"]}", \
                            form_apply_end = "{i["form_apply_end"]}"\
                            where form_no = {j["form_no"]};'
                    
                    base = db.cursor()
                    base.execute(sqll)
                    db.commit()
                    base.close()

                return {'updateMeet' : True}
            
            else:
                return {'updateMeet' : False}
        else:
            return { "updateMeet" : False}
            


