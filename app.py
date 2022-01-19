from flask import Flask
from flask_restx import Resource, Api

from User.createUser import createUser
from User.login import login

from Meet.seeMeet import seeMeet
from Meet.seeView import seeView

from Meet.inMeet import inMeet
from Meet.createMeet import createMeet

from Manage.seePartList import seePartList


app = Flask(__name__) # Flask 앱 생성
api = Api(app) # API 서버로 사용할 수 있게해줌.

api.add_namespace(createUser, '/createuser')
api.add_namespace(login, '/login')

api.add_namespace(seeMeet, '/seemeet')
api.add_namespace(seeView, '/seeview')


api.add_namespace(inMeet, '/inmeet')
api.add_namespace(createMeet, '/createmeet')

api.add_namespace(seePartList, '/seepartlist')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
