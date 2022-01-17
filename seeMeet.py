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

seeMeet = Namespace(
    name='seeMeet',
    description='seeMeet API'
)

@seeMeet.route('')
class SeeMeet(Resource):
    def get(self):

        db = setDB()

        # join = 모임에 신청자 수
        # where = 모집 기간이 지나기 전까지의 행사만
        # order by = 신청자 수 -> 상세 페이지 뷰 카운트 -> 최신 글 순서대로 정렬
        sql = f'select m.*, u.member from Meet as m \
                join (select meet_no, count(user_no) as member from MeetUser group by meet_no) as u \
                on m.meet_no = u.meet_no \
                where date(m.meet_recruit) > date(now())\
                group by m.meet_no, u.member\
                order by u.member desc, m.meet_view desc, m.meet_created desc;' 

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()

        if data:
            print(data)
    
        for i in data:
            i['meet_recruit'] = str(i['meet_recruit'])
            i['meet_created'] = str(i['meet_created'])
            i['meet_updated'] = str(i['meet_updated'])
        return { "List" : data}
    
@seeMeet.route('/detail/<string:meet_no>')
class seeMeetDetail(Resource):

    def get(self, meet_no):

        db = setDB()

        sql = f'select meet_no, meet_title, meet_total, meet_recruit, ( \
                    select count(user_no) as c from MeetUser \
                    where meet_no = {meet_no} \
                    group by meet_no) as meet_member \
                from Meet \
                where meet_no = {meet_no};'

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()

        sql = f'select f.* from Meet as m join Form as f \
                on m.meet_no = f.meet_no \
                where m.meet_no = {meet_no};'

        base = db.cursor()
        base.execute(sql)
        form = base.fetchall()
        base.close()

        for i in data:
            i['meet_recruit'] = str(i['meet_recruit'])
            
        for i in form:
            i['form_start'] = str(i['form_start'])
            i['form_end'] = str(i['form_end'])
            i['form_created'] = str(i['form_created'])
            i['form_updated'] = str(i['form_updated'])

        return {"Meet" : data[0], "Form" : form}