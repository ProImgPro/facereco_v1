from marshmallow import fields
from utils import parse_req
from flask import jsonify
from flask_restful import Resource
from bson import ObjectId
from werkzeug.security import safe_str_cmp
import pymongo
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_raw_jwt, jwt_required, get_jti)
from datetime import timedelta
from utils import check_email

# myclient = pymongo.MongoClient("mongodb://bootai:1234567aA%40@27.72.147.222:27017/erp?authSource=admin")
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mytable = myclient['test2m']
mycol = mytable['user']
mycol1 = mytable['token']

ACCESS_EXPIRES = timedelta(days=30)
FRESH_EXPIRES = timedelta(days=30)


class UserRegister(Resource):

    def post(self):

        param = {
            'username': fields.String(),
            'password': fields.String(),
            'email': fields.String()
        }
        try:
            json_data = parse_req(param)
            username = json_data.get('username', None)
            password = json_data.get('password', None)
            email = json_data.get('email', None)

        except Exception:
            return jsonify("An error occurred when getting data !")

        query_user = {
            '_id': str(ObjectId()),
            'username': username,
            'password': password,
            'email': email,
            'first_login': True
        }

        try:
            find_person = mycol.find_one({'username': username})
            if find_person is not None:
                return jsonify("Username is already exist")
            if check_email(email) is None:
                return jsonify("Invalidate email !")
            else:
                mycol.insert_one(query_user)
                return jsonify("Register successfully !")
        except Exception:
            return jsonify("An error occurred when inserting data !")


class Login(Resource):
    def post(self):
        param = {
            'username': fields.String(),
            'password': fields.String()
        }
        try:
            json_data = parse_req(param)
            username = json_data.get('username', None)
            password = json_data.get('password', None)
        except Exception:
            return jsonify("An error occurred when getting data !")

        user = mycol.find_one({'username': username})

        if not safe_str_cmp(user['password'], password):
            return jsonify("Your password is wrong !")

        access_token = create_access_token(identity=str(user['_id']), expires_delta=ACCESS_EXPIRES)
        fresh_token = create_refresh_token(identity=str(user['_id']), expires_delta=FRESH_EXPIRES)

        dict1 = {
            'access_token': access_token,
            'fresh_token': fresh_token,
            'message': 'Login Successfully !'
        }
        user_token = dict(
            _id=str(ObjectId()),
            person_id=user['_id'],
            access_token=access_token,
            fresh_token=fresh_token
        )
        mycol1.insert_one(user_token)
        if user['first_login'] is True:
            return jsonify(dict1)

        return jsonify(dict1)


class Logout(Resource):
    def delete(self):
        """

        :return:
        description: This method should be delete access_token from data base
        """
        access_token = get_raw_jwt()
        mycol1.remove({"access_token": access_token})
        return jsonify("Logout Successfully !")



