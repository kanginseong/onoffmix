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

inMeet = Namespace(
    name='inMeet',
    description='inMeet API'
)

@inMeet.route('/<string:meet_no>')
class InMeet(Resource):
    def post(self, meet_no):

        db = setDB()

        data = request.get_json()
        user_no = data['user_no']
        meet_reason = data['meet_reason']

        # 이미 들어간 방인지 확인
        sql = f'select user_no from MeetUser \
                where meet_no = "{meet_no}" and user_no = "{user_no}";'

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()

        
        if data:
            return {'inRoom': False}
        
        else:
            # 방이 개설자인지 아닌지 확인하기
            sql = f'select form_no, meet_no, form_admission \
                    from Form where meet_no = {meet_no};'

            sql = f'insert into Room_user(meet_no, user_no, meetuser_state)\
                values ("{meet_no}", "{user_no}", ,"N", "{meet_reason}");'

            base = db.cursor()
            base.execute(sql)
            db.commit()
            base.close()

            return {'inRoom': True}
    