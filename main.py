import os
import cv2
import time
import serial
import datetime
import multiprocessing
import subprocess
import signal
import face_recognition
import json
from flask import Flask, Response, render_template

COUNT_FRAME_WITH_DATA = 10


def StartWebServer(qI, port=5000):
    try:
        pid_to_kill = subprocess.check_output("fuser -n tcp 5000", shell=True)
        os.kill(int(pid_to_kill.decode()[1:]), signal.SIGKILL)
        time.sleep(2)
    except Exception:
        # fuser всегда ругается.
        pass
    app = Flask(__name__)

    def eventStream():
        while True:
            result = qI.get()
            yield 'data: %s\n\n' % str(result)

    @app.route("/stream")
    def stream():
        return Response(eventStream(), mimetype="text/event-stream")

    @app.route("/")
    def index():
        with open('templates/index.html', 'r') as index:
            ans = index.read()
            return ans

    app.run("", port)

def ConnectArduino(name):
    ser = serial.Serial('/dev/ttyACM3')
    ser.baudrate = 9600
    # ser = serial.Serial('COM3', 9600)
    time.sleep(2)
    print(name)
    ser.write(str.encode(name + '#'))

def CheckFace(cap, qI, window_name, count_frame):
    i = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow(window_name, img)
        if i % count_frame == 0:
            qI.put({'window_name': window_name, 'frame': img})
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
    cap.release()
    cv2.destroyAllWindows()


def FullRecognizedFace(qI, qO):
    # Загружаем все занкомые лица
    known_face_encodings = []
    known_face_names = []
    directory = os.getcwd() + '/DataSet'

    # Цикл для перебора всех изображений в папке
    for img in os.listdir(directory):
        path_to_image = directory + '/' + img
        image = face_recognition.load_image_file(path_to_image)
        face_encoding = face_recognition.face_encodings(image)[0]
        name = os.path.splitext(os.path.basename(path_to_image))[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)
    i = 0
    while True:
        data_frame = qI.get()
        window_name = data_frame.get('window_name')
        frame = data_frame.get('frame')
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name_p = 'Unknown'

            if True in matches:
                first_match_index = matches.index(True)
                name_p = known_face_names[first_match_index]
            # if i % 5 == 0:
            #     print('check')
            #     ConnectArduino(name)

            new_person = dict()
            new_person['name'] = name_p
            new_person['pic' ]= str(name_p)+'.png'
            new_person['time']= str(datetime.datetime.now())
            new_person['camera'] = window_name

            new_person_j = json.dumps(new_person)

            qO.put(new_person_j)
        i += 1




queueImg = multiprocessing.Queue()

queueToSend = multiprocessing.Queue()


# TODO: Надо выбрать между этими двумя алгоритмами. Мне больше зашел Fisher.
recognizer = cv2.face.FisherFaceRecognizer_create()

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FPS, 60)
prc = multiprocessing.Process(target=CheckFace, args=(cap, queueImg, 'Camera 1', COUNT_FRAME_WITH_DATA,))
prc.start()
print(prc.pid)

prc2 = multiprocessing.Process(target=StartWebServer, args=(queueToSend, ))
prc2.start()
print(prc2.pid)


FullRecognizedFace(queueImg, queueToSend)
print('12312')




