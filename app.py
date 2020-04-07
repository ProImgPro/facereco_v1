from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
import pymongo
from auth import UserRegister, Login, Logout
from Infor_User import Infor, ChangeAvatar, ListStudent
from flask_mail import Mail
from flask_restful import Resource
from DangKy_V1 import Registry
from NhanDien_V1 import Recognition, TimeAppear

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config["MONGO_URI"] = "mongodb://bootai:1234567aA%40@27.72.147.222:27017/erp?authSource=admin"
app.config["MONGO_URI"] = 'mongodb://localhost:27017/'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='manh.ngoxuan198@gmail.com',
    MAIL_PASSWORD='manhkorea1234'
)

mail = Mail(app)

jwt = JWTManager(app)

app.secret_key = 'Yep'

api = Api(app)

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mytable = myclient['test2m']
mycol2 = mytable['infor']
mycol3 = mytable['known_face_name']
mycol = mytable['user']


class SendMail(Resource):
    def get(self):
        find_name = mycol2.find_one({}, {'_id': 0, 'name': 1})
        find_name1 = mycol3.find_one({}, {'_id': 0, 'name': 1})

        find_email = mycol2.find_one({}, {'email': 1})
        if find_name == find_name1:
            msg = mail.send_message(
                'Roll Call Successfully !',
                sender='phaigiaunhuchungno198@gmail.com',
                recipients=[find_email['email']],
                body="Congratulations you've succeeded!"
            )
        return 'Mail sent'


api.add_resource(UserRegister, '/logup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Infor, '/infor')
api.add_resource(ChangeAvatar, '/change_avatar')
api.add_resource(SendMail, '/send_email')
api.add_resource(Registry, '/registry')
api.add_resource(Recognition, '/recognition')
api.add_resource(ListStudent, '/liststudent')
api.add_resource(TimeAppear, '/timeappear')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=23487, debug=True)
