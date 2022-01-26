from logging import fatal
import os
import pymysql
import json
import datetime
from flask_jwt_extended import *
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

seeRegiList = Namespace(
    name='seeRegiList',
    description='seeRegiList API'
)

# 그 방에 방장인지 확인

# 내가 만든 모임 확인

# 모임에 그룹들 확인

# 해당 그룹에서 참가자 확인

@seeRegiList.route('/meet')
class SeeRegiList(Resource):
    def get(self):
        
        user_no = getUser.whoami()

        db = setDB()

        # 그 방에 방장인지 확인을 해야한다.
        sql = f'select * from Meet where user_no = {user_no}; '

        base = db.cursor()
        base.execute(sql)
        meet = base.fetchall()
        base.close()

        for i in meet:
            i['meet_created'] = str(i['meet_created'])
            i['meet_updated'] = str(i['meet_updated'])

        return {"meet" : meet}

@seeRegiList.route('/group/<string:meet_no>')
class SeeRegiList(Resource):
    def get(self, meet_no):

        user_no = getUser.whoami()

        db = setDB()

        # 모임에 그룹들 확인
        sql = f'select * from Form where meet_no = {meet_no};'

        base = db.cursor()
        base.execute(sql)
        form = base.fetchall()
        base.close()

        for i in form:
            i['form_meet_start'] = str(i['form_meet_start'])
            i['form_meet_end'] = str(i['form_meet_end'])
            i['form_apply_start'] = str(i['form_apply_start'])
            i['form_apply_end'] = str(i['form_apply_end'])
            i['form_created'] = str(i['form_created'])
            i['form_updated'] = str(i['form_updated'])

        return {"group" : form}


@seeRegiList.route('/member/<string:form_no>')
class SeeRegiList(Resource):
    def get(self, form_no):

        user_no = getUser.whoami()

        db = setDB()

        # 모임에 그룹들 확인
        sql = f'select u.user_no, u.user_name, fu.form_reason, fu.formuser_state \
                from FormUser as fu join User as u on fu.user_no = u.user_no \
                where form_no = "{form_no}" and user_static= "P";'

        base = db.cursor()
        base.execute(sql)
        user = base.fetchall()
        base.close()

        return {"member" : user} 

            
        
