import cv2
import multiprocessing
import time


def checkEblo(cap, font, recognizer):
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y: y + h, x: x + w])
            if(conf < 30):
                if(Id == 1):
                    Id = "RYZYA"
                elif(Id == 2):
                    Id = "UMPALUMP"
                elif(Id == 3):
                    Id = "NASYINIKA"
                elif (Id == 4):
                    Id = "NAZYGORICH"
            else:
                print(str(Id))
                Id = "Unknown"
            #cv2.putText(img, str(Id), (x, y+h), font, 0.55, (0,255,0), 1)

        cv2.imshow('frame', img)
        if cv2.waitKey(3) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainner/trainner.yml')

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# cv2.namedWindow('frame')

font = cv2.FONT_HERSHEY_SIMPLEX
# cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# prc = multiprocessing.Process(target=checkEblo, args=(cap, font, recognizer, ))
# prc.start()
# print(prc.pid)

cap1 = cv2.VideoCapture(0)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap1.set(cv2.CAP_PROP_FPS, 60)
prc = multiprocessing.Process(target=checkEblo, args=(cap1, font, recognizer, ))
prc.start()
print(prc.pid)

time.sleep(3)

