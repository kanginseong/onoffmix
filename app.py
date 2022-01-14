from flask import Flask
from flask_restx import Resource, Api

from createUser import createUser
from login import login

app = Flask(__name__) # Flask 앱 생성
api = Api(app) # API 서버로 사용할 수 있게해줌.

api.add_namespace(createUser, '/createUsers')
api.add_namespace(login, '/logins')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
