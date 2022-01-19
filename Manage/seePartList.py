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

seePartList = Namespace(
    name='seePartList',
    description='seePartList API'
)

@seePartList.route('/<string:user_no>')
class SeePartList(Resource):
    def get(self, user_no):

        db = setDB()

        # 그 방에 방장인지 확인을 해야한다.
        sql = f'select m.* from FormUser as fu join Meet as m on fu.meet_no = m.meet_no where fu.user_no = {user_no} and fu.user_static="P";'

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()

        for i in data:
            i['meet_created'] = str(i['meet_created'])
            i['meet_updated'] = str(i['meet_updated'])

        return {"partList" : data}

# 모임을 검색하고 그 모임의 자세한 그룹 내용들 보기
# @seePartList.route('/detail/<string:meet_no>')
# class SeePartList(Resource):
#     def get(self, meet_no):

#         db = setDB()

#         # 모임에 그룹들 확인
#         sql = f'select form_no from FormUser where meet_no = {meet_no} group by form_no;'

#         base = db.cursor()
#         base.execute(sql)
#         data = base.fetchall()
#         base.close()
#         print(data)

#         # 해당 모임의 정보 확인
#         list = []
#         for i in data:
#             sqll = f'select * from FormUser as fu join Form as f on fu.form_no = f.form_no \
#                      where fu.form_no = "{i["form_no"]}" and ;'

#             base = db.cursor()
#             base.execute(sqll)
#             data = base.fetchall()
#             base.close()

#             for i in data:
#                 i['form_meet_start'] = str(i['form_meet_start'])
#                 i['form_meet_end'] = str(i['form_meet_end'])
#                 i['form_apply_start'] = str(i['form_apply_start'])
#                 i['form_apply_end'] = str(i['form_apply_end'])
#                 i['form_created'] = str(i['form_created'])
#                 i['form_updated'] = str(i['form_updated'])

#                 list.append(data)
            
#         return {"partList" : list}
            
        
