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

seeRegiList = Namespace(
    name='seeRegiList',
    description='seeRegiList API'
)

# 그 방에 방장인지 확인

# 내가 만든 모임 확인

# 모임에 그룹들 확인

# 해당 그룹에서 참가자 확인

@seeRegiList.route('/meet/<string:user_no>')
class SeeRegiList(Resource):
    def get(self, user_no):

        db = setDB()

        # 그 방에 방장인지 확인을 해야한다.
        sql = f'select meet_no from FormUser where user_no = {user_no} and user_static="M" group by meet_no'

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()

        return {"partList" : data}

@seeRegiList.route('/group/<string:meet_no>')
class SeeRegiList(Resource):
    def get(self, meet_no):

        db = setDB()

        # 모임에 그룹들 확인
        sql = f'select form_no from FormUser where meet_no = {meet_no} group by form_no;'

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()
        print(data)

        # 해당 그룹에서 참가자 확인
        list = []
        for i in data:
            sqll = f'select fu.meet_no, fu.form_no, fu.formuser_state, fu.form_reason, u.user_no, u.user_name \
                     from FormUser as fu join User as u on fu.user_no = u.user_no \
                     where form_no = "{i["form_no"]}" and user_static= "P";'

            base = db.cursor()
            base.execute(sqll)
            data = base.fetchall()
            base.close()

            list.append(data)
            
        return {"partList" : list}
            
        
