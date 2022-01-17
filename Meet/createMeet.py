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

createMeet = Namespace(
    name='createMeet',
    description='createMeet API'
)

@createMeet.route('')
class CreateMeet(Resource):
    def post(self):

        db = setDB()

        data = request.get_json()
        user_no = data['user_no']
        meet_title = data['meet_title']
        meet_content = data['meet_content']
        
        sql = f'insert into Meet(meet_title, meet_content, meet_view, user_no)\
                values ("{meet_title}", "{meet_content}", 0, {user_no});'
        base = db.cursor()
        base.execute(sql)
        db.commit()
        base.close()

        sql = f'select meet_no from Meet \
                where user_no = {user_no} and meet_title = "{meet_title}";'

        base = db.cursor()
        base.execute(sql)
        meet = base.fetchall()
        base.close()

        print(meet[0]['meet_no'])

        

        # group = data[{'form_title', 'form_total', 'form_admission', 'form_meet_start', 'form_meet_end', 'form_apply_start', 'form_apply_end', 'meet_no'}]

        # for i in group:
        #     sql = f'insert into Form(form_title, form_total, form_admission, form_meet_start, form_meet_end, form_apply_start, form_apply_end, meet_no) \
        #             values("{group[i][0]}", "{group[i][1]}", "{group[i][2]}", "{group[i][3]}", "{group[i][4]}", "{group[i][5]}", "{group[i][6]}", {meet});'