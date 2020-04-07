
import os
import cv2
import face_recognition
import pickle

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
            img_encoding = None
            try:
                img_encoding = face_recognition.face_encodings(img)[0]
            except:
                continue

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


def Lay_Thong_So_Mau():
    known_face_names , known_face_encodings = [], []
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

    return (known_face_names, known_face_encodings)


known_face_names, known_face_encodings = Lay_Thong_So_Mau()
cap = cv2.VideoCapture(0)
while True:

    ret, img = cap.read()
    # giảm kích thước để tăng tốc đô
    small_frame = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    rgb_img = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    for i in range(0, len(face_encodings), 1):
        face_encoding = face_encodings[i]

        max = 2
        name = "unknow"
        color = (0, 0, 255)
        for j in range(0, len(known_face_encodings), 1):
            chk = [known_face_encodings[j]]
            face_distances = face_recognition.face_distance(chk, face_encoding)

            if (max > face_distances[0]):
                max = face_distances[0]
                name = known_face_names[j]
                color = (0, 0, 0)
        max = round(max, 3)
        print(max, name)

        if max > 0.5:
            name = "unknow"
            color = (0, 0, 255)
        y1, x2, y2, x1 = face_locations[i]
        y1 = y1 *2
        x2 = x2 *2
        y2 = y2 *2
        x1 = x1 *2
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        # Draw a label with a name below the face
        cv2.rectangle(img, (x1 - 1, y2 + 20), (x2 + 1 , y2 ), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(max) +' ' + name, (x1 + 6, y2 + 20 - 6), font, 0.5, (255, 255, 255), 1)

    cv2.imshow("Video", img)
    if cv2.waitKey(2)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



