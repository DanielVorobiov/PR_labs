import socket
import json
import datetime
import cv2

faceCascade = cv2.CascadeClassifier(
    'data/haarcascade/haarcascade_frontalface_default.xml')
eyesCascade = cv2.CascadeClassifier('data/haarcascade/haarcascade_eye.xml')

video_capture = cv2.VideoCapture(0)

HOST = '127.0.0.1'
PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

eyes = []
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
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eyesCascade.detectMultiScale(roi_gray, 1.1, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0),
                          2)

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    data = {
        "Time": datetime.datetime.now().strftime("%Y : %m : %d - %H :%M:%S"),
        'Faces': len(faces),
        "Eyes": len(eyes)
    }
    data = json.dumps(data)
    data = data.encode()
    sock.sendto(data, (HOST, PORT))

sock.close()




