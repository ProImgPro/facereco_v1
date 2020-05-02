import cv2
import os
import face_recognition
import argparse
import pickle
from datetime import datetime


file_pickle_known_face_names = "known_face_names"
file_pickle_known_face_encodings = "known_face_encodings"


def Create_File_ThongSo():
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

    f_pickle_known_face_names = open(file_pickle_known_face_names, 'wb')
    pickle.dump(known_face_names, f_pickle_known_face_names)
    f_pickle_known_face_names.close()

    f_pickle_known_face_encodings = open(file_pickle_known_face_encodings, 'wb')
    pickle.dump(known_face_encodings, f_pickle_known_face_encodings)
    f_pickle_known_face_encodings.close()


    print("tạo file thông số hoàn tất")

# parser = argparse.ArgumentParser()
# parser.add_argument("--name", required=True)
# args = parser.parse_args()

#name = "Ngo Xuan Manh" # sửa tên rùi lấy mẫu
name = "Manh"
path = "data/"
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
    #code camera
    ret, img = cam.read()

    rgb_img = img[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_img)

    #nếu có đúng 1 khuông mặt thì lưu lại vào img_arr
    if len(face_locations) == 1:
        img_arr.append(img)

    cv2.imshow("Video", img)
    if cv2.waitKey(2) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()


known_face_encodings = []
known_face_names = []


while True:
    try:
        f_pickle_known_face_names = open(file_pickle_known_face_names, 'rb')
        known_face_names = pickle.load(f_pickle_known_face_names)
        f_pickle_known_face_names.close()

        f_pickle_known_face_encodings = open(file_pickle_known_face_encodings, 'rb')
        known_face_encodings = pickle.load(f_pickle_known_face_encodings)
        f_pickle_known_face_encodings.close()

        break
    except:
        print("chưa có file thông số, bắt đầu tạo")
        Create_File_ThongSo()


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
    known_face_encodings.append(img_encoding)
    known_face_names.append(name)


f_pickle_known_face_names = open(file_pickle_known_face_names, 'wb')
pickle.dump(known_face_names, f_pickle_known_face_names)
f_pickle_known_face_names.close()

f_pickle_known_face_encodings = open(file_pickle_known_face_encodings, 'wb')
pickle.dump(known_face_encodings, f_pickle_known_face_encodings)
f_pickle_known_face_encodings.close()

print("đã ghi xong dữ liệu")
