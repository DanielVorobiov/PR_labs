import socket
import time
import json
import datetime
import cv2

faceCascade = cv2.CascadeClassifier(
    'data/haarcascade/haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

HOST = '127.0.0.1'
PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

i = 0
while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
    print(faces)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 0)
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    data = {
        "Time": datetime.datetime.now().strftime("%Y : %m : %d - %H :%M:%S"),
        'Faces': len(faces)
    }
    data = json.dumps(data)
    data = data.encode()
    sock.send(data)

    i += 1

sock.close()
