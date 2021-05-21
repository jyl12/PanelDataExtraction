import numpy as np
import cv2
import APP_opcua
from random import randint

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

server = APP_opcua.ExtendedServer(4840)
node = server.get_objects_node()
print("node is:", node)
param = node.add_object(server.addspace, "Parameters")
print("param is:",param)
Temp = param.add_variable (server.addspace, "detected", 0)
server.start()
print("Server is started at {}".format(server.url))

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #print(len(faces))
    Temp.set_value(1,6)#len(faces)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        # eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        # for (ex, ey, ew, eh) in eyes:
        #     cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()