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

createGroup = Namespace(
    name='createGroup',
    description='createGroup API'
)

@createGroup.route('')
class CreateGroup(Resource):
    def post(self):

        db = setDB()

        data = request.get_json()
        form_title = data['form_title']
        form_total = data['form_total']
        form_admission = data['form_admission']
        form_meet_start = data['form_meet_start']
        form_meet_end = data['form_meet_end']
        form_apply_start = data['form_apply_start']
        form_apply_end = data['form_apply_end']
        meet_no = data['meet_no']

        base = db.cursor()

        sql = f'insert into Form(form_title, form_total, form_admission, form_meet_start, form_meet_end, form_apply_start, form_apply_end, meet_no) \
                values("{form_title}", {form_total}, "{form_admission}", "{form_meet_start}", "{form_meet_end}", "{form_apply_start}", "{form_apply_end}", {meet_no});'
        base.execute(sql)
        db.commit()
        base.close()

        return {'createGroup' : True}