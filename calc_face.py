import cv2
import face_recognition

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# video_capture.set(cv2.CAP_PROP_FPS, 60)

ryz_image = face_recognition.load_image_file("DataSet/ryz.png")
ryz_face_encoding = face_recognition.face_encodings(ryz_image)[0]

egg_image = face_recognition.load_image_file("DataSet/egg.png")
egg_face_encoding = face_recognition.face_encodings(egg_image)[0]

misha_image = face_recognition.load_image_file("DataSet/misha.png")
misha_face_encoding = face_recognition.face_encodings(misha_image)[0]

aleks_image = face_recognition.load_image_file("DataSet/barg.png")
aleks_face_encoding = face_recognition.face_encodings(aleks_image)[0]

nat_image = face_recognition.load_image_file("DataSet/nat.png")
nat_face_encoding = face_recognition.face_encodings(nat_image)[0]


known_face_encodings = [ryz_face_encoding,
                        egg_face_encoding,
                        misha_face_encoding,
                        aleks_face_encoding,
                        nat_face_encoding]
known_face_names = ["RUZGE", "NAZI_EGG", "NASINIKA", "Aleksey", "Natasha"]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

