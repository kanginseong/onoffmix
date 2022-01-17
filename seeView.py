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

seeView = Namespace(
    name='seeView',
    description='seeView API'
)

@seeView.route('/<string:meet_no>')
class SeeView(Resource):

    def get(self, meet_no):

        db = setDB()

        sql = f'update Meet \
                set meet_view = (select meet_view) + 1 \
                where meet_no = {meet_no};'

        base = db.cursor()
        base.execute(sql)
        db.commit()
        base.close()

        return { "View" : True }