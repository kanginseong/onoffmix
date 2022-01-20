from distutils.debug import DEBUG
from flask import Flask
from flask_restx import Resource, Api
from flask_jwt_extended import *

from User.createUser import createUser
from User.login import login

from Meet.seeMeet import seeMeet
from Meet.updateView import updateView

from Meet.inMeet import inMeet
from Meet.createMeet import createMeet

from Manage.seeRegiList import seeRegiList
from Manage.updateRegiList import updateRegiList
from Manage.seePartList import seePartList

app = Flask(__name__) # Flask 앱 생성

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "I'M IML"
)

jwt = JWTManager(app)

api = Api(app) # API 서버로 사용할 수 있게해줌.

api.add_namespace(createUser, '/createuser')
api.add_namespace(login, '/login')

api.add_namespace(seeMeet, '/seemeet')
api.add_namespace(updateView, '/updateview')

api.add_namespace(inMeet, '/inmeet')
api.add_namespace(createMeet, '/createmeet')

api.add_namespace(seeRegiList, '/seeregilist')
api.add_namespace(updateRegiList, '/updateregilist')
api.add_namespace(seePartList, '/seepartlist')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
