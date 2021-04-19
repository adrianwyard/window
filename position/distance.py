import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
from win32api import GetSystemMetrics

screenWidth = int(GetSystemMetrics(0))
screenHeight = int(GetSystemMetrics(1))

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

camera_capture = cv2.VideoCapture(0)
video_capture = cv2.VideoCapture('video/2.mp4')

width, height = int(camera_capture.get(3)), int(camera_capture.get(4))
out = cv2.VideoWriter("1.mp4", cv2.VideoWriter_fourcc(*"DIVX"), 30.0, (width, height))
anterior = 0

known_distance1 = 4.3
known_width1 = 48

known_distance2 = 2.2
known_width2 = 107

focalLength = known_distance1*known_width1

while True:
    # Capture frame-by-frame
    ret, frame = camera_capture.read()
    ret1, frame1 = video_capture.read()


    if not ret:
        print("can't load image")
        break
    if not ret1:
        video_capture = cv2.VideoCapture('video/2.mp4')
        continue

    frame1 = cv2.resize(frame1, (screenWidth, screenHeight), interpolation = cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    faceWidthList = []
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        faceWidthList.append(w)

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
    if len(faces) > 0:
        index = faceWidthList.index(max(faceWidthList))
        distance = focalLength/faces[index][2]

        blue = None
        if distance <= 0.6:
            blur = frame1
        else:
            blur = cv2.GaussianBlur(frame1, (0, 0), distance/0.2-3)

        cv2.putText(blur, "%.2fM" % (focalLength/faces[index][2]),
            (blur.shape[1] - 200, blur.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 255, 0), 2)

        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("window", blur)

    # Display the resulting frame
        out.write(blur)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
camera_capture.release()
cv2.destroyAllWindows()
