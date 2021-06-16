import numpy as np
import cv2
import APP_opcua
import B3.seven_seg
from random import randint
from imutils.video import VideoStream
import datetime
import imutils
import time

# ***** OPCUA *****
# server = APP_opcua.ExtendedServer(4840)
# node = server.get_objects_node()
# print("node is:", node)
# param = node.add_object(server.addspace, "Parameters")
# print("param is:",param)
# Temp = param.add_variable (server.addspace, "detected", 0)
# server.start()
# print("Server is started at {}".format(server.url))
# ***** OPCUA *****

# initialize the video streams and allow them to warmup
print("[INFO] starting cameras...")
webcam = VideoStream(src=0).start()
#picam = VideoStream(usePiCamera=True).start()
# image = cv2.imread(r"C:\Users\Inspiron\Downloads\PanelDataExtraction\B3\example.jpg")
time.sleep(2.0)
test =1
while True:

    if test == 1:
        # initialize the list of frames that have been processed
        frames = []
        # read the next frame from the video stream and resize
        # it to have a maximum width of 400 pixels
        frame = webcam.read()
        # frame = imutils.resize(frame, width=400)
        cam7seg = B3.seven_seg.seven_seg_disp(frame)
        # # draw the timestamp on the frame
        # timestamp = datetime.datetime.now()
        # ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        # cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        #     0.35, (0, 0, 255), 1)
        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    if test == 2:
        cap = cv2.VideoCapture(r'C:\Users\Inspiron\Documents\Git\camb\PanelDataExtraction\PanelDataExtraction\B3\examplejpg-MyVideo-Convert2video-com.mp4')
        if (cap.isOpened() == False):
            print("cannot open")
        while True:
            ret, frame = cap.read()
            cam7seg = B3.seven_seg.seven_seg_disp(frame)
            cv2.imshow("frame",frame)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
cv2.destroyAllWindows()
webcam.stop()
