import pymysql
from flask_jwt_extended import *
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

@jwt_required()
def whoami():

    cur_user = get_jwt_identity()
    user = cur_user[0]['user_no']

    if user:
        return user
    else:
        return {"getUser" : "doesn't matching"}