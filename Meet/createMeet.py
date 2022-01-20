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

createMeet = Namespace(
    name='createMeet',
    description='createMeet API'
)

@createMeet.route('')
class CreateMeet(Resource):
    def post(self):
        
        user_no = getUser.whoami()

        db = setDB()

        data = request.get_json()
        
        meet_title = data['meet_title']
        meet_content = data['meet_content']
        
        sql = f'select meet_title from Meet\
                where meet_title = "{meet_title}";'
        base = db.cursor()
        base.execute(sql)
        check = base.fetchall()
        base.close()

        if check:
            return { "createMeet" : False}

        else:
            # 모임이 만들어지면
            sql = f'insert into Meet(meet_title, meet_content, meet_view, user_no)\
                    values ("{meet_title}", "{meet_content}", 0, {user_no});'
            base = db.cursor()
            base.execute(sql)
            db.commit()
            base.close()

            # 그 모임의 pk를 불러와
            sql = f'select meet_no from Meet \
                    where user_no = {user_no} and meet_title = "{meet_title}";'

            base = db.cursor()
            base.execute(sql)
            meet = base.fetchall()
            base.close()
            meet = meet[0]['meet_no']
            
            group = data['group']

            for i in group:            
                sqll = f'insert into Form(form_title, form_total, form_admission, form_meet_start, form_meet_end, form_apply_start, form_apply_end, meet_no) \
                        values("{i["form_title"]}", {i["form_total"]}, "{i["form_admission"]}", "{i["form_meet_start"]}", "{i["form_meet_end"]}", "{i["form_apply_start"]}", "{i["form_apply_end"]}", {meet});'
                            
                print(sqll)
                
                base = db.cursor()
                base.execute(sqll)
                db.commit()
                base.close()

                sql = f'select form_no from Form\
                        where form_title = "{i["form_title"]}";'
                base = db.cursor()
                base.execute(sql)
                form = base.fetchall()
                base.close()

                form = form[0]['form_no']

                base = db.cursor()
                sqll = f'insert into FormUser(meet_no, form_no, user_no, user_static, formuser_state)\
                         values ({meet}, {form}, {user_no}, "M", "Y");'
                base.execute(sqll)
                db.commit()
                base.close()

            return {'createMeet' : True}


