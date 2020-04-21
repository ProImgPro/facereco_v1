import os
from flask import jsonify, request
from flask_restful import Resource
from marshmallow import fields
from utils import parse_req, PATH_AVATAR, PATH_AVATAR_SERVER, allow_file_img, AVATAR_DEFAULT
from bson import ObjectId
from flask_jwt_extended import jwt_required, JWTManager
from werkzeug.utils import secure_filename
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import get_jwt_claims
import pymongo
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

mail = Mail(app)

jwt = JWTManager(app)


# myclient = pymongo.MongoClient("mongodb://bootai:1234567aA%40@27.72.147.222:27017/erp?authSource=admin")
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mytable = myclient['test2m']
mycol2 = mytable['infor']
mycol3 = mytable['known_face_name']
mycol = mytable['user']


class Infor(Resource):

    def post(self):

        """
        :variable: name, age, course, name_class
        :return:
        description: This method should create information of people
        """

        # person_id = request.args.get('_id', None)
        # query = {
        #     '_id': person_id
        # }
        # find_person = mycol2.find_one(query)
        # if find_person is None:
        #     return jsonify("No data !")
        #
        # if find_person['group_id'] != '1':
        #     return jsonify("You don;t have permission to manipulate this performance !")

        param = {
            'name': fields.String(),
            'age': fields.Number(),
            'course': fields.String(),
            'number_student': fields.String(),
            'name_class': fields.String(),
            'group_id':  fields.String(),
            'email': fields.String()

        }

        try:
            json_data = parse_req(param)
            name = json_data.get('name', None)
            age = json_data.get('age', None)
            course = json_data.get('course', None)
            number_student = json_data.get('number_student', None)
            name_class = json_data.get('name_class', None)
            group_id = json_data.get('group_id', None)
            email = json_data.get('email', None)
        except Exception as e:
            return jsonify("An error occurred when getting data")

        query_user = {
            '_id': str(ObjectId()),
            'name': name,
            'age': int(age),
            'course': course,
            'number_student': number_student,
            'name_class': name_class,
            'file_avatar': None,
            'thumbnail': PATH_AVATAR_SERVER + AVATAR_DEFAULT,
            'group_id': group_id,
            'email': email
        }

        try:
            mycol2.insert_one(query_user)
            return jsonify("Insert Successfully !")
        except Exception:
            return jsonify("An error occurred when inserting data")

    @jwt_required
    def put(self):
        """
        :variable: name, age, course, name_class
        :return:
        description: This method should update information of people
        """
        person_id = request.args.get('_id', None)
        query = {
            '_id': person_id
        }
        find_person = mycol2.find_one(query)
        if find_person is None:
            return jsonify("No data !")

        if find_person['group_id'] != '1':
            return jsonify("You don;t have permission to manipulate this performance !")

        person_id = request.args.get('_id', None)
        param = {
            'name': fields.String(),
            'age': fields.Number(),
            'course': fields.String(),
            'number_student': fields.String(),
            'name_class': fields.String()
        }

        try:
            json_data = parse_req(param)
            name = json_data.get('name', None)
            age = json_data.get('age', None)
            number_student = json_data.get('number_student', None)
            course = json_data.get('course', None)
            name_class = json_data.get('name_class', None)
        except Exception as e:
            return {e}
        query = {
            '_id': person_id
        }
        try:
            find_person = mycol2.find_one(query)
            if find_person is None:
                return jsonify("No data !")
        except Exception:
            return jsonify("An error occurred when finding data !")

        new_query = {
            '$set': {
                'name': name,
                'age': int(age),
                'course': course,
                'number_student': number_student,
                'name_class': name_class
                }
        }
        try:
            mycol2.update_one(query, new_query)
            return jsonify("Update successfully !")
        except Exception:
            return jsonify("An error occurred when updating data")

    def get(self):
        """
        :param: page_size, page_number
        :return:
        description: this method should return all the student
        """
        person_id = request.args.get('_id', None)
        query = {
            '_id': person_id
        }
        find_person = mycol2.find_one(query)
        if find_person is None:
            return jsonify("No data !")

        if find_person['group_id'] != '1':
            return jsonify("You don;t have permission to manipulate this performance !")

        page_size = request.args.get('page_size', '25')
        page_number = request.args.get('page_number', '0')
        skips = int(page_size) * int(page_number)
        find_data = list(mycol2.find({}, {'_id': 0}).skip(skips).limit(int(page_size)))
        return jsonify(find_data)

    @jwt_required
    def delete(self):
        """
        :param: _id
        :return:
        description: This method should delete a student
        """
        person_id = request.args.get('_id', None)
        query = {
            '_id': person_id
        }
        find_person = mycol2.find_one(query)
        if find_person is None:
            return jsonify("No data !")

        if find_person['group_id'] != '1':
            return jsonify("You don;t have permission to manipulate this performance !")

        person_id = request.args.get('_id', None)
        query_id = {
            '_id': person_id
        }
        try:
            mycol2.remove(query_id)
            return jsonify("Delete Successfully !")
        except Exception:
            return jsonify("An error occurred when deleting data !")


class ChangeAvatar(Resource):

    @jwt_required
    def put(self):
        person_id = request.args.get('_id', None)
        query = {
            '_id': person_id
        }
        find_person = mycol2.find_one(query)
        if find_person is None:
            return jsonify("No data !")

        if find_person['group_id'] != '1':
            return jsonify("You don;t have permission to manipulate this performance !")

        person_id = request.args.get('_id', None)
        find_person = mycol2.find_one({'_id': person_id})
        if find_person is None:
            return jsonify("No data. This person haven't exist yet !")

        try:
            profile_img = request.files['image']
        except Exception:
            return jsonify("An error occurred when requesting files !")


        filename = profile_img.filename
        filename = find_person['name'] + filename
        filename = secure_filename(filename)
        if find_person['file_avatar'] is not None:
            list_file = os.listdir(PATH_AVATAR)
            for i in list_file:
                if safe_str_cmp(i, find_person['file_avatar']):
                    os.remove(os.path.join(PATH_AVATAR, i))

        path = os.path.join(PATH_AVATAR, filename)
        path_server = os.path.join(PATH_AVATAR_SERVER, filename)
        try:
            profile_img.save(path)
        except Exception:
            return jsonify("An error occurred when saving data !")

        new_value = {
            '$set': {
                'thumbnail': path_server,
                'file_avatar': filename
            }
        }
        try:
            mycol2.update_one({'_id': person_id}, new_value)
            return jsonify("Change image successfully !")
        except Exception:
            return jsonify("Error occurred when updating image")


class ListStudent(Resource):
    def get(self):
        students = mycol2.find({})
        if not students:
            return jsonify("No data !")
        results = []
        for student in students:
            results.append(student)

        return jsonify(results)





