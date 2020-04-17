import cv2
import os
import face_recognition
import pickle
import pymongo
from flask import jsonify, request, Flask
from datetime import datetime
from flask_restful import Resource
from flask_jwt_extended import JWTManager
from flask_restful import Api


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config["MONGO_URI"] = "mongodb://bootai:1234567aA%40@27.72.147.222:27017/erp?authSource=admin"
app.config["MONGO_URI"] = 'mongodb://localhost:27017/'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

jwt = JWTManager(app)

app.secret_key = 'Yep'

api = Api(app)

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mytable = myclient['test2m']
mycol2 = mytable['infor']
mycol4 = mytable['registry']


class Registry(Resource):
    known_face_encodings = []
    known_face_names = []
    file_pickle_known_face_names = "known_face_names"
    file_pickle_known_face_encodings = "known_face_encodings"

    @classmethod
    def Create_File_ThongSo(cls):
        path = "data/"
        ThongTin = list(os.walk(path))

        # tạo mảng dữ liệu
        known_face_encodings = []
        known_face_names = []
        known_face_Filenames = []

        # đưa dữ liệu vào mảng
        for i in range(1, len(ThongTin), 1):
            for infor in ThongTin[i][2]:
                name = ThongTin[0][1][i - 1]
                image = infor
                full_path = path + name + "/"

                img = face_recognition.load_image_file(full_path + image)
                img_encoding = face_recognition.face_encodings(img)[0]

                known_face_names.append(name)
                known_face_encodings.append(img_encoding)
                known_face_Filenames.append(image)

        f_pickle_known_face_names = open(cls.file_pickle_known_face_names, 'wb')
        pickle.dump(known_face_names, f_pickle_known_face_names)
        f_pickle_known_face_names.close()

        f_pickle_known_face_encodings = open(cls.file_pickle_known_face_encodings, 'wb')
        pickle.dump(known_face_encodings, f_pickle_known_face_encodings)
        f_pickle_known_face_encodings.close()

        print("tạo file thông số hoàn tất")

    @classmethod
    def get(cls):
        # param = request.args.get('name', None)
        # find_name = mycol2.find_one({'name': param}, {'_id': 0, 'name':1})
        # if find_name is None:
        #     return jsonify("No data!")
        #
        # name = str(find_name['name'])

        path = "data/"
        name = "OOO"
        dirName = path + name

        try:
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        except FileExistsError:
            print("Directory ", dirName, " already exists")

        frame_name = 0
        img_arr = []

        cam = cv2.VideoCapture(0)

        while True:
            # code camera
            ret, img = cam.read()

            rgb_img = img[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_img)

            # nếu có đúng 1 khuôn mặt thì lưu lại vào img_arr
            if len(face_locations) == 1:
                img_arr.append(img)

            cv2.imshow("Video", img)
            if cv2.waitKey(2) == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        while True:
            try:
                f_pickle_known_face_names = open(cls.file_pickle_known_face_names, 'rb')
                known_face_names = pickle.load(f_pickle_known_face_names)
                f_pickle_known_face_names.close()

                f_pickle_known_face_encodings = open(cls.file_pickle_known_face_encodings, 'rb')
                known_face_encodings = pickle.load(f_pickle_known_face_encodings)
                f_pickle_known_face_encodings.close()

                break
            except:
                print("chưa có file thông số, bắt đầu tạo")
                cls.Create_File_ThongSo()

        now = datetime.now()
        Ngay = now.strftime("%d")
        Thang = now.strftime("%m")
        Nam = now.strftime("%y")
        current_time = now.strftime("%H:%M:%S")
        ThoiGian = Ngay+Thang+Nam+current_time

        for img in img_arr:
            cv2.imwrite(dirName + "/" + ThoiGian + str(frame_name) + ".jpg", img)
            frame_name = frame_name + 1

            img_encoding = face_recognition.face_encodings(img)[0]
            cls.known_face_encodings.append(img_encoding)
            cls.known_face_names.append(name)

        f_pickle_known_face_names = open(cls.file_pickle_known_face_names, 'wb')
        pickle.dump(known_face_names, f_pickle_known_face_names)
        f_pickle_known_face_names.close()

        f_pickle_known_face_encodings = open(cls.file_pickle_known_face_encodings, 'wb')
        pickle.dump(known_face_encodings, f_pickle_known_face_encodings)
        f_pickle_known_face_encodings.close()

        return jsonify("Create Successfully !")


api.add_resource(Registry, '/res')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2345, debug=True)


