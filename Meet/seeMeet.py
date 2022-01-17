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
        sql = f'select m.meet_no, m.meet_title, m.meet_created, m.meet_content, m.meet_view, f.form_no, form_title, u.member from Form as f \
                inner join (select form_no, count(user_no) as member from FormUser group by form_no) as u \
                on f.form_no = u.form_no \
                join Meet as m \
                on f.meet_no = m.meet_no \
                where date(f.form_meet_end) > date(now()) \
                group by f.form_no, u.member \
                order by u.member desc, m.meet_view desc, m.meet_created desc;' 

        base = db.cursor()
        base.execute(sql)
        data = base.fetchall()
        base.close()
    
        for i in data:
            i['meet_created'] = str(i['meet_created'])

        return { "List" : data}
    
@seeMeet.route('/detail/<string:meet_no>')
class seeMeetDetail(Resource):

    def get(self, meet_no):

        db = setDB()

        sql = f'select meet_no, meet_title, meet_created, meet_view, \
                    (select count(user_no) as c from FormUser \
                     where meet_no = {meet_no} \
                     group by meet_no) as meet_member \
                from Meet \
                where meet_no = {meet_no};'

        base = db.cursor()
        base.execute(sql)
        meet = base.fetchall()
        base.close()

        sql = f'select f.* from Meet as m right join Form as f \
                on m.meet_no = f.meet_no \
                where m.meet_no = {meet_no};'

        base = db.cursor()
        base.execute(sql)
        form = base.fetchall()
        base.close()

        for i in meet:
            i['meet_created'] = str(i['meet_created'])

        for i in form:
            i['form_meet_start'] = str(i['form_meet_start'])
            i['form_meet_end'] = str(i['form_meet_end'])
            i['form_apply_start'] = str(i['form_apply_start'])
            i['form_apply_end'] = str(i['form_apply_end'])
            i['form_created'] = str(i['form_created'])
            i['form_updated'] = str(i['form_updated'])

        return {"Meet" : meet[0], "Form" : form}