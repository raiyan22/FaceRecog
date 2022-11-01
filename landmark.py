# https://pysource.com/2019/03/12/face-landmarks-detection-opencv-with-python/

import cv2 as cv
import numpy as np
import dlib


cap = cv.VideoCapture(0)
# capWebcam = cv.VideoCapture(0)

#  https://github.com/davisking/dlib-models

# predictor to detect face
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_81_face_landmarks.dat')

# url = 'http://192.168.0.6:8080/video'

# cap.open(url)

while True :
    _ , frame = cap.read()
    # _ , frameWebcam = capWebcam.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # grayWebcam = cv.cvtColor(frameWebcam, cv.COLOR_BGR2GRAY)

    faces = detector(gray)
    # facesWebcam = detector(grayWebcam)

    # print(faces)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

    # for face in facesWebcam:
    #     x11 = face.left()
    #     y11 = face.top()
    #     x22 = face.right()
    #     y22 = face.bottom()

        # bounding box
        # cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)

        landmarks = predictor(gray, face)
        # landmarksWebcam = predictor(grayWebcam, face)
        # print(landmarks)
        
        # x = landmarks.part(30).x
        # y = landmarks.part(30).y
        # print(x,y)
        # cv.circle(frame,(x,y),3,(255,0,0),-1)

        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv.circle(frame, (x, y), 4, (255, 0, 0), -1)

        # for n in range(0, 68):
        #     x1 = landmarksWebcam.part(n).x
        #     y1 = landmarksWebcam.part(n).y
        #     cv.circle(frameWebcam, (x1, y1), 4, (255, 0, 0), -1)


    cv.imshow('frame',frame)
    # cv.imshow('frameWebcam',frameWebcam)
    key = cv.waitKey(1)
    if key == ord('d'):
        break
