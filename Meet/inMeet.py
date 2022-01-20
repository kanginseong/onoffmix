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

inMeet = Namespace(
    name='inMeet',
    description='inMeet API'
)

@inMeet.route('')
class InMeet(Resource):
    def post(self):

        user_no = getUser.whoami()

        db = setDB()

        data = request.get_json()
        meet_no = data['meet_no']
        form_no = data['form_no']
        meet_reason = data['meet_reason']

        # 이미 들어간 모임인지 확인
        
        sql = f'select user_no from FormUser\
            where meet_no = {meet_no} and user_no = {user_no};'

        base = db.cursor()
        base.execute(sql)
        check = base.fetchall()
        base.close()

        
        if check:
            return {'inMeet': False}
        
        # 정원이 찼는지 안찼는지 검사
        else:

            sql = f'select form_no from Form \
                    where form_no = {form_no} and form_total <= \
                    (select count(user_no) as c from FormUser  where meet_no = {meet_no} group by meet_no);'

            base = db.cursor()
            base.execute(sql)
            check = base.fetchall()
            base.close()

            if check:
                return {"inMeet" : False}

            else:
            # 방이 개설자인지 선착순인지 아닌지 확인하기
                sql = f'select form_no, meet_no, form_admission \
                        from Form where form_no = {form_no};'

                base = db.cursor()
                base.execute(sql)
                type = base.fetchall()
                base.close()
                
                if type:
                    for i in type:
                        ## 개설자 - 개설자한테 승인을 받아야함
                        if i['form_admission'] == "G":
                            sql = f'insert into FormUser(meet_no, form_no, user_no, user_static, formuser_state, form_reason)\
                                    values ({meet_no}, {form_no}, {user_no}, "P", "N", "{meet_reason}");'

                            base = db.cursor()
                            base.execute(sql)
                            db.commit()
                            base.close()

                            return {'inMeet': "G"}
                            
                        
                        ## 선착순 - 참여 인원 보고 가능하면 바로 Y
                        elif i['form_admission'] == "S":
                            sql = f'insert into FormUser(meet_no, form_no, user_no, user_static, formuser_state, form_reason)\
                                    values ({meet_no}, {form_no}, {user_no}, "P", "Y", "{meet_reason}");'

                            base = db.cursor()
                            base.execute(sql)
                            db.commit()
                            base.close()

                            return {'inMeet': "S"}