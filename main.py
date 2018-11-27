import os
import cv2
import multiprocessing
import face_recognition


def CheckFace(cap, qI, qN):
    i = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('frame', img)
        if i % 100 == 0:
            qI.put(img)
        if cv2.waitKey(3) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def FullRecognizedFace(qI, qN):
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

    while True:
        small_frame = cv2.resize(qI.get(), (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = 'Unknown'

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            qN.put(name)
            print('Name = ' + str(name))


queueImg = multiprocessing.Queue()
queueName = multiprocessing.Queue()


# TODO: Надо выбрать между этими двумя алгоритмами. Мне больше зашел Fisher.
recognizer = cv2.face.FisherFaceRecognizer_create()

# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read('trainner/trainner.yml')

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
prc = multiprocessing.Process(target=CheckFace, args=(cap, queueImg, queueName, ))
prc.start()
print(prc.pid)

prc2 = multiprocessing.Process(target=FullRecognizedFace, args=(queueImg, queueName, ))
prc2.start()
print(prc2.pid)




