from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDialog, QMessageBox, QFileDialog, QComboBox, QTableWidget
from PyQt5.QtCore import QSequentialAnimationGroup, QTimer, QTime , Qt, QDate, QDateTime, QRect
from PyQt5.QtGui import QIcon, QImage, QPixmap, QBrush, QPainter,QWindow, QImage, QPixmap
from PyQt5.uic import loadUi
import sys
import os 
import requests
import sqlite3
import firebaseAuth as fba
import datetime
import cv2 as cv
# required for marking attendance
import numpy as np
import face_recognition 
from numpy.lib.function_base import append
import csv

self.markattendance_err_label.setText("Loading ...")
        
            # cap = cv.VideoCapture(0)

            encodeListKnown = self.findEncodings( self.images)
            print('[LOG] Encoding DONE')

            cap = cv.VideoCapture(0)

            self.cam_is_on = True
            # check further same csv exist kore ki na
            csv_created = False
            arr = []
            for i in range(125):
                        arr.append(0)

            # while ( cap.isOpened() ):
            while ( self.logic == 0 ):
              ret, frame = cap.read()

              if ret == True:
                self.markattendance_err_label.setText("Taking Attendance...")

                self.display_the_img(frame,1)

                imgSmall = cv.resize(frame,(0,0),None, 0.25,0.25)
                imgSmall = cv.cvtColor(imgSmall, cv.COLOR_BGR2RGB)

                facesCurrentFrame = face_recognition.face_locations(imgSmall)
                encodesCurrentFrame = face_recognition.face_encodings(imgSmall, facesCurrentFrame)
                for encodeFace, faceLoc in zip(encodesCurrentFrame,facesCurrentFrame):
                  matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                  faceDistance = face_recognition.face_distance(encodeListKnown,encodeFace)
                  #print(faceDistance) # the lesser the distance the best match it is 
                  matchIndex = np.argmin(faceDistance)
                
                  if matches[matchIndex]:
                      classNames = self.classNames
                      s_name = classNames[ matchIndex ]
                      name = ''
                      #  print(s_name)
          
                      name = s_name.split('_')[0]

                      roll2 = name[4]+name[5]+name[6]

                      idx = int(roll2)

                      now = datetime.datetime.now()
                      pth = now.strftime('%I:%M:%S')
                      day = now.strftime('%d').strip()
                      mon = now.strftime('%m').strip()
                      year = now.strftime('%Y')
                      mon2 = mon
                      day2 = day

                      if mon2[0]=='0':
                        mon3 = mon2[1]
                        mon=mon3
                      if day[0] == '0':
                        day3 = day[1]
                        day=day3

                      conn = sqlite3.connect("Attendance_System.db")
                      cc = conn.cursor()
                      data = (name,self.course_code,day,mon,year,pth)
                      
                      if arr[idx] == 0:

                          cc.execute("INSERT INTO Atten VALUES(?,?,?,?,?,?)", data)
                      conn.commit()
                      conn.close()
                      arr[idx]=1

                      
                      
                        

            
                      y1, x2, y2, x1 = faceLoc
                      y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                      cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                      # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
                      cv.putText(frame,name,(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                      self.display_the_img(frame,1)
          
                      # self.markAttendance(name, csv_filename)

                      print("[LOG] " + name + " attended")
                  else:
                      y1, x2, y2, x1 = faceLoc
                      y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                      cv.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                      # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
                      cv.putText(frame,'Unknown',(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                      print("[LOG] Unknown Face Detected")
                      self.display_the_img(frame,1)

              k = cv.waitKey(1)