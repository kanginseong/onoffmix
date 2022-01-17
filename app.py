from flask import Flask
from flask_restx import Resource, Api

from User.createUser import createUser
from User.login import login

from Meet.seeMeet import seeMeet
from Meet.seeView import seeView

from Meet.inMeet import inMeet

from Meet.createMeet import createMeet
from Meet.createGroup import createGroup

app = Flask(__name__) # Flask 앱 생성
api = Api(app) # API 서버로 사용할 수 있게해줌.

api.add_namespace(createUser, '/createUser')
api.add_namespace(login, '/login')

api.add_namespace(seeMeet, '/seeMeet')
api.add_namespace(seeView, '/seeView')

api.add_namespace(inMeet, '/inMeet')

api.add_namespace(createMeet, '/createMeet')
api.add_namespace(createGroup, '/createGroup')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
