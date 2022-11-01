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


# https://www.programiz.com/python-programming/datetime/strptime 

class ManualAttendance(QMainWindow):

  global day, mon, yr
  day = 1 
  mon = datetime.datetime.now().month  # gives "6", not "06"
  yr = datetime.datetime.now().year # gives "2021"

  def __init__(self,user):
    super(ManualAttendance,self).__init__()
    loadUi('UI/manualattendance.ui',self)

    self.cal.setGridVisible(True)
        # print(day, mon, yr)
        # to view a certain date preselected on cal by default
    self.cal.setSelectedDate(QDate(yr,mon, day))

    self.user = user

    self.course_code_list = []
    list_course_code = []
    self.dept = ""
    self.selected_date = ""
    self.selected_month = ""
    self.selected_year = ""
    self.selected_course_code = ""
    
    conn = sqlite3.connect("Attendance_System.db")
    cc = conn.cursor()
    data22 = self.user['email'] 
    cc.execute("SELECT course_no FROM Course_Alloc WHERE email=?", [data22] )
    box1=cc.fetchall()
    cc.execute("SELECT dept FROM Course_Alloc WHERE email=?", [data22] )
    self.dept = cc.fetchone()  # ('CSE',)
    try:
      self.dept = self.dept[0]   # CSE
    except:
      print("[LOG] no course")

    for i in box1:
        if i[0] not in list_course_code:
          list_course_code.append(i[0])
        
    self.course_code_list = list_course_code

    conn.commit()
    conn.close()
    
    self.course_code_cbox.addItem("Click to select")
    self.course_code_cbox.addItems(list_course_code)

    self.course_code_cbox.currentIndexChanged.connect(self.updateCombo)

    self.cal.clicked.connect( self.getDate )
    self.add_data_btn.clicked.connect( self.add_data )
    self.backtodashboard_btn.clicked.connect( self.gobacktodashboard )
    

  def getDate(self, qDate):
    self.selected_date = qDate.day()
    self.selected_month = qDate.month()
    self.selected_year = qDate.year()
    print('[LOG] date selected', self.selected_date,self.selected_month, self.selected_year)

  def updateCombo(self, index1):
    self.selected_course_code = self.course_code_cbox.itemText(index1)

  def add_data(self):
    roll2 = self.add_roll_input.text().strip().replace(" ","")
    list_roll = roll2.split(",")
    for ee in list_roll:
      print(ee)
    ln = len(list_roll)
    print(ln)  
    for iii in range(ln):
      roll = list_roll[iii]
      if ( self.selected_course_code!="Click to select" and roll!=""):
        
        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        data22 = [ roll, self.selected_course_code, self.selected_date,self.selected_month, self.selected_year, "00:00:00"]

        cc = conn.cursor()
        cc.execute("INSERT INTO Atten VALUES(?,?,?,?,?,?)", data22)
        conn.commit()
        conn.close()
        print('[LOG] manually added->', data22)
        self.show_data_lbl.setText("Added successfully")
        
            
      else:
          self.show_data_lbl.setText("Please Enter Roll, Course Code & Date correctly")
      
  def gobacktodashboard(self):
    
    self.mainappwindow = MainAppWindow( self.user )

    widget.addWidget(self.mainappwindow)
    widget.setFixedSize(770,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

    print('[LOG] ' + self.user['email'] + ' got back to the dashboard successfully' )

class ShowAttendance(QMainWindow):

  global day, mon, yr
  day = 1  # gives "10"
  mon = datetime.datetime.now().month  # gives "6", not "06"
  yr = datetime.datetime.now().year # gives "2021"

  def __init__(self,user):
    super(ShowAttendance,self).__init__()
    loadUi('UI/showattendance.ui',self)

    self.cal.setGridVisible(True)
        # print(day, mon, yr)
        # to view a certain date preselected on cal by default
    self.cal.setSelectedDate(QDate(yr,mon, day))

    self.user = user

    self.course_code_list = []
    list_course_code = []
    
    self.dept = ""
    self.selected_date = ""
    self.selected_month = ""
    self.selected_year = ""
    self.selected_course_code = ""
    
    conn = sqlite3.connect("Attendance_System.db")
    cc = conn.cursor()
    data22 = self.user['email'] 
    cc.execute("SELECT course_no FROM Course_Alloc WHERE email=?", [data22] )
    box1=cc.fetchall()
    cc.execute("SELECT dept FROM Course_Alloc WHERE email=?", [data22] )
    self.dept = cc.fetchone()  # ('CSE',)
    self.dept = self.dept[0]   # CSE
    
    for i in box1:
        if i[0] not in list_course_code:
          list_course_code.append(i[0])
          
    list_ultimate = []
    list_ultimate = list_course_code
        
    self.course_code_list = list_ultimate

    conn.commit()
    conn.close()
    
    self.course_code_cbox.addItem("Click to select")
    self.course_code_cbox.addItems(list_ultimate)

    fields = [ "Roll No.", "Time"]
    self.tableWidget.setHorizontalHeaderLabels(fields)

    self.course_code_cbox.currentIndexChanged.connect(self.updateCombo)

    self.tableWidget.setColumnWidth(0,130)
    self.tableWidget.setColumnWidth(1,130)
    # self.tableWidget.setColumnWidth(2,100)
    # self.tableWidget.setGeometry(10,20)
    self.cal.clicked.connect( self.getDate )
    self.show_data_btn.clicked.connect( self.load_data )
    self.show_data_btn_2.clicked.connect( self.load_count )
    self.export_csv_btn.clicked.connect( self.export_csv_func )
    self.backtodashboard_btn.clicked.connect( self.gobacktodashboard )
    
    
    # WORK
    # self.select_date_comboBox
    # self.select_courseCode_comboBox


  def load_count(self):
        fields = [ "Roll No.", "Total_Count"]
        self.tableWidget.setHorizontalHeaderLabels(fields)
        self.tableWidget.clear()
        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        data22 = [ self.selected_course_code]
        m = cc.execute("SELECT roll FROM Atten where course_no=?", data22)
        arr= []
        for ii in range(125):
          arr.append(0)
        for item in m:
          #print(item)
          jj = item[0]

          print(jj)

          roll2 = jj[4]+jj[5]+jj[6]
          roll = int(roll2)
          print(roll)
          arr[roll] +=1

        number_of_rows_fetched = 0 
        m = cc.execute("SELECT roll FROM Atten where course_no=?", data22)
        for i in m:
          number_of_rows_fetched += 1
          print(number_of_rows_fetched)
        # print('row')
        # print(number_of_rows_fetched)
        if ( number_of_rows_fetched == 0 ):
            print('[LOG] fetched',number_of_rows_fetched, "row(s)" )
            self.show_data_lbl.setText("No Data to fetch for given info")
            if ( self.selected_course_code!="Click to select" ):
                self.show_data_lbl.setText("Please select course code")
                
                self.tableWidget.setRowCount( 0 )

        else:
          m = cc.execute("SELECT * FROM Atten where course_no=?", data22)
          
          print('[LOG] fetched',number_of_rows_fetched, "row(s)" )
          self.tableWidget.setRowCount( number_of_rows_fetched )
          
          m = cc.execute("SELECT * FROM Atten where course_no=?", data22)
          tableindex = 0
          roll_check = []
          for iii in range (125):
            roll_check.append(0)
          for record in m :
            print("REC ")
            print(record)
            roll2 = record[0]
            print("roll2: ")
            print(roll2)
            tt = roll2[4]+roll2[5]+roll2[6]
            roll = int(tt)
            print("roll: ")
            print(roll)
            timing = arr[roll]
            print("timing:")
            print(timing)
            prpr = str(timing)
            if roll_check[roll] == 0:
              self.tableWidget.setItem( tableindex, 0, QtWidgets.QTableWidgetItem(  roll2  ) )
              self.tableWidget.setItem(tableindex, 1, QtWidgets.QTableWidgetItem(  prpr  ) )
            tableindex += 1
            roll_check[roll] += 1
          self.show_data_lbl.setText("Success")
          
        


          
        conn.commit()
        conn.close()



  def export_csv_func(self):
      if ( self.selected_course_code!="Click to select" ):
        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        data22 = [ self.selected_course_code, self.selected_date,self.selected_month, self.selected_year]
        m = cc.execute("SELECT * FROM Atten where (course_no,date,mon,year)=(?,?,?,?)", data22)

        srl=1
        fields = ["Serial No.", "Roll No.", "Time"]
        datestring = str(self.selected_date) + "-" + str(self.selected_month) + "-" + str(self.selected_year)

        with open("{}-{}.csv".format(self.selected_course_code,datestring), 'w', newline='') as file:
              writer = csv.writer(file)
              writer.writerow(fields)

        each_row = []

        arr = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
              
        for lst in m:
            roll = lst[0]
            ptt = lst[5]
            roll2 = roll[4]+roll[5]+roll[6]
            idx = int(roll2)
            print(idx)
            # print(roll+" "+ptt)
            if(arr[idx] == 0):
                each_row.append( [ srl,roll,ptt ] )
            srl+=1
            arr[idx] = 1   

        with open("{}-{}.csv".format(self.selected_course_code,datestring), 'a', newline='') as file:
              writer = csv.writer(file)
              writer.writerows(each_row)

        conn.commit()
        conn.close()
      else:
        self.show_data_lbl.setText("Please Select Date & Course Code correctly")
  
  def getDate(self, qDate):
    self.selected_date = qDate.day()
    self.selected_month = qDate.month()
    self.selected_year = qDate.year()
    print('[LOG] date selected', self.selected_date,self.selected_month, self.selected_year)

  def updateCombo(self, index1):
    
    self.selected_course_code = self.course_code_cbox.itemText(index1)
    self.selected_course_code = self.selected_course_code

  def load_data(self):
    fields = [ "Roll No.", "Time"]

    self.tableWidget.setHorizontalHeaderLabels(fields)
    self.tableWidget.clear()
    if ( self.selected_course_code!="Click to select" ):
      
      conn = sqlite3.connect("Attendance_System.db")
      cc = conn.cursor()
      data22 = [ self.selected_course_code, self.selected_date,self.selected_month, self.selected_year]
      # print( data22)  
      m = cc.execute("SELECT * FROM Atten where (course_no,date,mon,year)=(?,?,?,?)", data22)

      # FEROT 
      number_of_rows_fetched = 0 
      for i in m:
        number_of_rows_fetched += 1
      # print('row')
      # print(number_of_rows_fetched)
      if ( number_of_rows_fetched == 0 ):
          print('[LOG] fetched',number_of_rows_fetched, "row(s)" )
          self.show_data_lbl.setText("No Data to fetch for given info")
          if ( self.selected_course_code!="Click to select" ):
              self.show_data_lbl.setText("Please select course code")
              self.tableWidget.setRowCount( 0 )

      else:
        m = cc.execute("SELECT * FROM Atten where (course_no,date,mon,year)=(?,?,?,?)", data22)
        
        print('[LOG] fetched',number_of_rows_fetched, "row(s)" )
        self.tableWidget.setRowCount( number_of_rows_fetched )
        tableindex = 0
        for record in m :
          roll = record[0]
          timing = record[5]
          self.tableWidget.setItem( tableindex, 0, QtWidgets.QTableWidgetItem(  roll  ) )
          self.tableWidget.setItem(tableindex, 1, QtWidgets.QTableWidgetItem(  timing  ) )
          tableindex += 1
        self.show_data_lbl.setText("Success")
        conn.commit()
        conn.close()
    else:
        self.show_data_lbl.setText("Please Select Date & Course Code correctly")
      
  def gobacktodashboard(self):
    
    self.mainappwindow = MainAppWindow( self.user )

    widget.addWidget(self.mainappwindow)
    widget.setFixedSize(770,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

    print('[LOG] ' + self.user['email'] + ' got back to the dashboard successfully' )

class MarkAttendance(QMainWindow):
  def __init__(self,user ):
    super(MarkAttendance,self).__init__()
    loadUi('UI/markattendance.ui',self)

    self.logic = 0
    self.cam_is_on = False
    self.user = user

    conn = sqlite3.connect("Attendance_System.db")
    cc = conn.cursor()
    # cc.execute("DELETE FROM Student" ) 
    cc.execute("""
        CREATE TABLE IF NOT EXISTS Atten (
            roll text,
            course_no text,
            date text,
            mon text,
            year text,
            pth text
        )
    """)


    data22 = user['email'] 
    cc.execute("SELECT course_no FROM Course_Alloc WHERE email=?", [data22] )
    box1=cc.fetchall()

    box1unique = [] # contains unique course codes
    for i in box1:
      if i not in box1unique:
        box1unique.append(i[0])

    # folders = [] contains name of folders downloaded from db that matches with available course_no
    # this is to prevent downloading an empty file, sir er course set kora hoise but 
    # kono student oi course e registered nai so student er kono picture thakbe na, eta prevent korar jonno 
    folders = [] 

    all_files = os.listdir()
    for file in all_files:
      if( file in box1unique):
        folders.append(file)

    conn.commit()
    conn.close()

    print(folders) # ei ei folder gula download kora hoise egulai mark-attend cbox e show kora hobe
    
    self.course_code = ""
    self.path = ""
    self.images = []
    self.classNames = []
    self.myList = []
    self.cache_data = []
    self.csv_filename = ""
    self.row_count = 0

    self.course_code_cbox.addItem("Click to select")
    # *** IMPORTANT ***
    # self.course_code_cbox.addItems(self.course_code_list) # fetched from db 
    self.course_code_cbox.addItems(folders) # fetched from os.listdir() if downloaded
    

    self.img_label.setText("")
    self.backtodashboard_btn.clicked.connect( self.gobacktodashboard )

    self.start_attendance_btn.clicked.connect( self.showwebcam_btn_function )
    self.stop_attendance_btn.clicked.connect( self.stop_webcam_btn_function )

    self.course_code_cbox.currentTextChanged.connect(self.on_coursecode_change_func)
    # self.course_code_cbox.currentTextChanged.connect( self.on_combobox_text_change_func )

    # self.path = str( self.course_code_cbox.currentText() )

    # print(self.myList) # names of image files

    
    # print(classNames) # names of image files without extension

    #  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  def on_coursecode_change_func(self, course_code ):

    self.course_code = course_code
    self.path = course_code
    print('[LOG]', course_code, 'selected')
    if(self.path != "Click to select") :
      try :
        self.myList = os.listdir( self.path )
        self.markattendance_err_label.setText("")

        for cl in self.myList:
          currentImg = cv.imread(f'{self.path}/{cl}')
          self.images.append(currentImg)
          self.classNames.append(os.path.splitext(cl)[0] )
      except:
          print('[LOG] select coursse code')

    
      # self.images = []
      # self.classNames = []
      # self.myList = []

  def stop_webcam_btn_function(self):
    if (self.cam_is_on ) :
      self.logic = 3
      self.markattendance_err_label.setText("Stopped Taking Attendance...")

  def showwebcam_btn_function(self):
    if ( self.course_code!="Click to select" ):
        print('[LOG] Encoding START')

        # now = datetime.datetime.now()
        # dtString = now.strftime('%d-%m-%Y')
        
        # csv_filename = '{}-{}'.format(self.course_code,dtString)
        #     # MAIN TOKEN

        # fields = ["Serial No.", "Roll No.", "Time"]

        # with open("{}.csv".format( csv_filename ), 'w', newline='') as file:
        #       writer = csv.writer(file)
        #       writer.writerow(fields)

        # from datetime import datetime


        def eye_aspect_ratio(eye):
          # compute the euclidean distances between the two sets of
          # vertical eye landmarks (x, y)-coordinates
          A = dist.euclidean(eye[1], eye[5])
          B = dist.euclidean(eye[2], eye[4])
          # compute the euclidean distance between the horizontal
          # eye landmark (x, y)-coordinates
          C = dist.euclidean(eye[0], eye[3])
          # compute the eye aspect ratio
          ear = (A + B) / (2.0 * C)
          # return the eye aspect ratio
          return ear



        EYE_AR_THRESH = 0.3
        EYE_AR_CONSEC_FRAMES = 3
        COUNTER = 0
        TOTAL = 0
        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_81_face_landmarks.dat')
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


        self.markattendance_err_label.setText("Loading ...")
    
        # cap = cv.VideoCapture(0)

        encodeListKnown = self.findEncodings( self.images)
        print('[LOG] Encoding DONE')

        cap = cv.VideoCapture(0, cv.CAP_DSHOW)

        self.cam_is_on = True
        # check further same csv exist kore ki na
        csv_created = False
        arr = []
        for i in range(125):
                    arr.append(0)
        count = 0
        # while ( cap.isOpened() ):
        while ( self.logic == 0 ):
          
          ret, frame = cap.read()

          if ret == True:
            self.markattendance_err_label.setText("Taking Attendance...")

            self.display_the_img(frame,1)




            frame2 = cv.resize(frame,(0,0),None, 0.25,0.25)
            gray = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
            rects = detector(gray, 0)
            for rect in rects:
              shape = predictor(gray, rect)
              shape = face_utils.shape_to_np(shape)
              leftEye = shape[lStart:lEnd]
              rightEye = shape[rStart:rEnd]
              leftEAR = eye_aspect_ratio(leftEye)
              rightEAR = eye_aspect_ratio(rightEye)
              ear = (leftEAR + rightEAR) / 2.0
              leftEyeHull = cv.convexHull(leftEye)
              rightEyeHull = cv.convexHull(rightEye)
              cv.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
              cv.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
              if ear < EYE_AR_THRESH:
                COUNTER += 1
              else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                  TOTAL += 1
                COUNTER = 0
              cv.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
              cv.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
         




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

                  

                  
                  
                    

        
                  y1, x2, y2, x1 = faceLoc
                  y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                  cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                  # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
                  cv.putText(frame,name,(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                  self.display_the_img(frame,1)
      
                  # self.markAttendance(name, csv_filename)
                  if TOTAL >= 2:
                    conn = sqlite3.connect("Attendance_System.db")
                    cc = conn.cursor()
                    data = (name,self.course_code,day,mon,year,pth)
                    if arr[idx] == 0:
                      cc.execute("INSERT INTO Atten VALUES(?,?,?,?,?,?)", data)
                    conn.commit()
                    conn.close()  
                    arr[idx]=1
                    print("[LOG] " + name + " attended")
                    TOTAL = 0
              else:
                  y1, x2, y2, x1 = faceLoc
                  y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                  cv.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                  # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
                  cv.putText(frame,'Unknown',(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                  print("[LOG] Unknown Face Detected")
                  self.display_the_img(frame,1)

          k = cv.waitKey(1)

            # if( self.logic == 2 ):

            
            # if   k%256 == ord('p'):
          if  self.logic == 3 :
               break 

        # cap.close()
        # cap.release()
        # cv.destroyAllWindows()
        self.logic = 0
        
        self.markattendance_err_label.setText(" Attendance Taken successfully ")
        self.img_label.setText("")

    else:
      self.markattendance_err_label.setText("Please Choose the Course Code first")
    
    
  def display_the_img(self,img,w):
    # displaying the webcam on the label 

    # reference ot this entire f()
    # https://www.youtube.com/watch?v=iA45JnQh3Ow&ab_channel=OceanofMathematics%26Technology

    # image = cv.resize(img, (640, 480)) eta k half kore disi
    image = cv.resize(img, (320, 240))

    # https://doc.qt.io/qt-5/qimage.html#Format-enum
    ########### BUJHI NAI EGLA NICHER LINES ... SEE THIS LINK

    qformat = QImage.Format_Indexed8
    if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
    outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
    outImage = outImage.rgbSwapped()
    self.img_label.setPixmap(QPixmap.fromImage(outImage))
    self.img_label.setScaledContents(True)

  def on_combobox_text_change_func(self, course_code):
    # if (course_code != "Click to select"):
    #   self.course_code = course_code
    #   self.markattendance_err_label.setText("")
    # else:
    #   print("[LOG] select course code first")
    #   self.markattendance_err_label.setText("Please Choose the Course Code first")
    pass

  def gobacktodashboard(self):
    self.logic = 3
    # data = (roll,course_no,date,mon,year,pth)

    print('[LOG] saved to db')
    self.mainappwindow = MainAppWindow( self.user )

    widget.addWidget(self.mainappwindow)
    widget.setFixedSize(770,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

    print('[LOG] ' +self.user['email'] + ' went back to the dashboard successfully' )

  def findEncodings(self, images ):
    encodeList = []
    for img in self.images :
      img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
      encode = face_recognition.face_encodings(img)[0]
      encodeList.append(encode)

    print('[LOG] Encoding in progress ... ')
    return encodeList
  
  def markAttendance(self, name, csv_filename):

    now = datetime.datetime.now()
    day = now.strftime('%d').strip()
    mon = now.strftime('%m').strip()
    year = now.strftime('%Y')

    with open(f'{csv_filename}.csv','r+') as f:

      myDataList = f.readlines()
      namelist = []
      for line in myDataList:
        entry = line.split(',')
        namelist.append(entry[0])
      if name not in namelist:
        self.row_count+=1
        now = datetime.datetime.now()
        TIMEString = now.strftime('%I:%M:%S')
        f.writelines(f'\n{self.row_count},{name},{TIMEString}')

        data = (name, self.course_code ,day,mon,year,TIMEString)

        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        # data = (roll,course_no,date,mon,year,pth)

        cc.execute("INSERT INTO Atten VALUES(?,?,?,?,?,?)", data)
        conn.commit()
        conn.close()



class MainAppWindow(QMainWindow):
  def __init__(self,user):
    super(MainAppWindow,self).__init__()
    loadUi('UI/dashboard.ui',self)

    self.u = user
    self.selected_course_code = ""
    self.welcome_label.setText(self.u['email'])

    self.logout_btn.clicked.connect( self.logout )
    self.markattendance_btn.clicked.connect( self.gotomarkattendance )
    self.showattendance_btn.clicked.connect( self.gotoshow_attendance )
    self.add_attendance_manually_btn.clicked.connect( self.goto_add_manually )
    # self.confirm_btn.clicked.connect( self.download_func )
    # self.confirm_btn.setIcon( QtGui.QIcon("downdown.png"))
    

    self.course_code_list = []
    list_course_code = []
    self.dept = ""
    
    conn = sqlite3.connect("Attendance_System.db")
    cc = conn.cursor()
    data22 = self.u['email'] 
    # print(data22)
    cc.execute("SELECT course_no FROM Course_Alloc WHERE email=?", [data22] )
    box1=cc.fetchall()
    cc.execute("SELECT dept FROM Course_Alloc WHERE email=?", [data22] )
    self.dept = cc.fetchone()  # ('CSE',)
    # print(self.dept)
    try :
        self.dept = self.dept[0]   # CSE
    except:
        
        print("[LOG] No course was assigned for current email")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('No course was assigned by admin for current user')
        msg.setWindowTitle("No Course assigned!")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    # print(self.dept)

    # print("box1 e je oi teach er shob course info gula choila aise dehaitesi:")

    for i in box1:
        if i[0] not in list_course_code:
          list_course_code.append(i[0])
        
    # print(list_course_code)
    self.course_code_list = list_course_code

    self.download_func()

    conn.commit()
    conn.close()
    
    # TOKENNN
    # self.course_code_cbox.addItem("Click to select")
    # self.course_code_cbox.addItems(list_course_code)

    # self.course_code_cbox.currentIndexChanged.connect(self.updateCombo)

    ### Q T I M E R #######
    
    timer = QTimer(self)
    timer.timeout.connect( self.displayTime )
    timer.start(1000)

    self.showUser()
        
    

  def download_func(self):
      #self.selected_course_code = "CSE3117-DEF"
      conn = sqlite3.connect("Attendance_System.db")

      cc = conn.cursor()
      data22 = [self.u['email']]
      m=cc.execute("SELECT course_no from Course_Alloc where email=?",data22)

      list_course = []

      for data in m:

        print(data[0])
        list_course.append(data[0])


      conn.commit()
      conn.close()
      for tt in list_course:
        self.selected_course_code = tt
        if (self.selected_course_code != "Click to select" ):
          print('[LOG] downloading data for', self.selected_course_code )
          conn = sqlite3.connect("Attendance_System.db")

          # TOKEN DOWNLOAD

          cc = conn.cursor()
          data22 = [ self.selected_course_code ]
          m = cc.execute("SELECT * FROM Student where course_no = ?", data22)
          # count_row = cc.execute("SELECT COUNT(*) FROM Student where course_no = ?", data22)

          # print( count_row )

          path=os.getcwd()
          os.chdir(path)
          if not os.path.exists(self.selected_course_code):
            os.mkdir( self.selected_course_code )

          c = 0
          for x in m:
              roll    = x[0]
              # dept    = x[1]
              # course  = x[2]
              rec_data= x[3]
              cc = str(c)
              c+=1
              print("Eije: ")
              print(cc)
              with open(self.selected_course_code+'/'+ roll+'_'+ cc +'.jpg', 'wb') as f:
                  f.write(rec_data) 

          if(c==0):
            # means there was no data to fetch from db 
            os.rmdir(self.selected_course_code)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('No data to found for selected course code' )
            msg.setWindowTitle("Enter Email")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            print("[LOG] No data to fetch for", self.selected_course_code )

          conn.commit()
          conn.close()

        else : 
          print("[LOG] select course code to continue")

  def updateCombo(self, index1):
    
    self.selected_course_code = self.course_code_cbox.itemText(index1)
    self.selected_course_code = self.selected_course_code.replace(" ","")

  def goto_add_manually(self):
    
    showAttendance = ManualAttendance(self.u)
    widget.addWidget(showAttendance)
    widget.setFixedSize(780,590)
    widget.setCurrentIndex( widget.currentIndex()+1 )

  def gotoshow_attendance(self):
    # if there is atleast one csv file inh attendance then you are allowed to go o/w it gives error
    showAttendance = ShowAttendance(self.u)
    widget.addWidget(showAttendance)
    widget.setFixedSize(780,590)
    widget.setCurrentIndex( widget.currentIndex()+1 )

  def displayTime(self):
    #  use QDateTime better ig 
    # https://stackoverflow.com/questions/49623210/how-to-convert-qtime-12-to-24-hr-format-and-viceversa
    currentTime = QTime.currentTime()
    now = QDate.currentDate()
    displayText = currentTime.toString('h:mm:ss ap')
    displayTextDate = now.toString('dd/MM/yy')

    self.time_label.setText(displayText)
    self.date_label.setText(displayTextDate)

  def gotomarkattendance(self):

    markattendance = MarkAttendance(self.u)
    widget.addWidget(markattendance)
    widget.setFixedSize(780,590)
    
    widget.setCurrentIndex(widget.currentIndex()+1)

  def showUser(self):
    print('[LOG] ' +self.u['email'] + ' got into the dashboard successfully' )

  def logout_confirmation(self, i):

    # if OK button is clicked then logout
    if ( i.text() == "OK" ):
      # FIX THIS
      fba.authentication.requests.close() ####################
  
      login = Login()
      widget.addWidget(login)
      widget.setFixedSize(470,570)
      widget.setCurrentIndex(widget.currentIndex()+1)
      print('[LOG] ' + self.u['email'] + ' logged out')
      # print('[LOG]' + self.u['email'] + ' logged out') #########################
      self.u = {} #########################################

  def logout(self):
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)

    msg.setText('Are you sure to Logout?')
          # msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Logout Confirmation")
          # msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.setDefaultButton(QMessageBox.Cancel)
    msg.buttonClicked.connect(self.logout_confirmation)
	
    retval = msg.exec_()






class RegisterStudentsViaAdmin(QMainWindow):
  def __init__(self,user):
    super(RegisterStudentsViaAdmin,self).__init__()
    loadUi('UI/registerstudentsviaadmin.ui',self)
    
    self.number_of_img_captured = 0
    self.user = user
    self.logic = 0

    self.name = ""
    self.roll = ""
    self.course_no = ""
    self.dept = ""
    self.captured = False
    self.webcam_is_on = False
    self.chosen_images_dir_list = []
    # self.student_name = ""
    self.backtodashboard_btn.clicked.connect( self.gobacktodashboard )

    self.showwebcam_btn.clicked.connect( self.showwebcam_btn_function )
    self.stop_webcam_btn.clicked.connect( self.stop_webcam_btn_function )
    self.capture_btn.clicked.connect( self.capture_btn_function )
    self.submit_btn.clicked.connect( self.submitRegistration ) 
    self.bulk_btn.clicked.connect( self.bulk )
    #self.ulk.clicked.connect( self.bulk_reg )

    

    

        # ALL DEPARTMENT DB THEKE FETCH
    
    
                

  


    

    

    
    
    # self.comboBox.setPlaceholderText("Select Department")        KAAJ KORE NA :(
    
    # combobox er functionalties check below 
    # https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm



  def bulk(self):
        print("GG")
        # WE CAN CHOOSE A CSV FILE FROM OUR HARD DISK VIA THIS FUNCTION 
        fname_tuple = QFileDialog.getOpenFileName(self, 'Open file', 'D:\hello', ' ( *.csv)') # this is the default directory 
        filename = fname_tuple[0] # WITHOUT EXTENSION
        
        try :
            with open(filename, mode ='r')as file:
                
                csvFile = csv.reader(file)

                for lines in csvFile:  # 1707022,CSE,CSE3200-TOC,CSE3400-REF
                  # ROLL at 0th column
                  # DEPT at 1th column

                  roll = lines[0]        # 1707022
                  dept = lines[1]         # CSE
                  courses_enrolled = lines[2:]     # list of courses to be enrolled for certain roll

                  # print(roll,dept, courses_enrolled) 

                  # 1707022 CSE ['CSE3200-TOC', 'CSE3400-REF', 'CSE3232-FFG']
                  # 5678 CSE ['CSE3200-TOC', 'CSE3400-REF']

                  # 1707022 er joto images ase root e shobdi ailo
                  list_of_name_of_images_to_be_saved_in_db = [x for x in os.listdir('root/images/') if roll in x]
                  
                  if (courses_enrolled!="") :

                      conn = sqlite3.connect("Attendance_System.db")
                      cc = conn.cursor()
 
                      for item in list_of_name_of_images_to_be_saved_in_db:
                        print('image name: ' + item) 
                        jj = item         # IMAGE ER NAAM TA 
                        with open( str( 'root/images/' + jj ) , 'rb') as f:
                          Img = f.read()

                          for courses in courses_enrolled:
                              print(courses)
                              conn = sqlite3.connect("Attendance_System.db")

                              cc = conn.cursor()

                              data = (roll,dept,courses,Img)
                              print(data[0])
                              print(data[1])
                              print(data[2])
                              cc.execute("INSERT INTO Student VALUES (?,?,?,?)", data)
                              conn.commit() 
                              conn.close()
                        
                          print(roll, dept ,jj )

                          # DB TE RAKHA LAGBE 

                          data = [(roll,Img),]

                          # cc.executemany("INSERT INTO Student VALUES (?,?,?,?)", data)     
                          # cc.execute("INSERT INTO Student VALUES (?,?,?,?)", data) 
                           
                            
                      
                    # print("got roll", roll)

                # displaying the contents of the CSV file
                # for lines in csvFile:
                #     if dept in lines:
                #        print(lines)
                        
        except:
            print('user closed the file dialog')
    

  def capture_btn_function(self):
    if ( self.webcam_is_on ):
      self.logic = 2
  
  def stop_webcam_btn_function(self):
    if ( self.webcam_is_on ):
      self.logic = 3

  def showwebcam_btn_function(self):

    # observation :
    #  chosen img er indexing 1 theke but captured img er indexing 0 theke kora hoise 

      #   make sure shuru tei stop e click kore keu jeno show webcam er kaaj e beghat na ghotaye -_-
      # self.logic 0 thakbe first e 
      # show webcam w click korle self logic  ???
      # capture btn e  click korle self logic  ???
      # stop e click korle self logic  ??? 

      # check if self logic == 0 ? keep on showing each frame 
      # check if self logic == 2 ? capture 
      # check if self logic == 3 ? stop capture and self logic 0 korbo just like it was before

    
    name = self.name_input.text()
    roll = self.roll_input.text()

    # combo box theke dept+course no input 
    self.name = name.strip()
    self.roll = roll
    
    
    

    if ( self.name and self.roll  ):

        self.webcam_is_on = True
        cap = cv.VideoCapture(0)
        self.registerstudents_err_label.setText("")

        # while ( cap.isOpened() ):
        while ( self.logic == 0 ):
          ret, frame = cap.read()
          if ret == True:

            self.display_the_img(frame,1)

            k = cv.waitKey(1)

            if( self.logic == 2 ):

              # Path = 'root/images/%s_%s.png'%(self.name_input.text().strip().replace(" ",""),str(self.i))
              Path = 'root/images/%s_%s_%s.jpg'%(self.name.strip().replace(" ",""), self.roll ,str(self.number_of_img_captured))

              print('[LOG] saved image at ' + Path)
              self.number_of_img_captured  = self.number_of_img_captured + 1
              cv.imwrite(Path, frame)
              self.captured = True

              self.logic = 0
              self.registerstudents_err_label.setText( str(self.number_of_img_captured ) +" Image(s) saved :)")
            
            # if   k%256 == ord('p'):
            if  self.logic == 3 :
              break 

        # cap.close()
        # cap.release()
        # cv.destroyAllWindows()
        self.logic = 0
        
        self.registerstudents_err_label.setText(" Webcam is Closed now ")
        self.img_label.setText("")

    else:
      self.registerstudents_err_label.setText("Please Enter required data first")
    
    

  def display_the_img(self,img,w):
    # displaying the webcam on the label 

    # reference ot this entire f()
    # https://www.youtube.com/watch?v=iA45JnQh3Ow&ab_channel=OceanofMathematics%26Technology

    # image = cv.resize(img, (640, 480)) eta k half kore disi
    image = cv.resize(img, (320, 240))

    # https://doc.qt.io/qt-5/qimage.html#Format-enum
    ########### BUJHI NAI EGLA NICHER LINES ... SEE THIS LINK

    qformat = QImage.Format_Indexed8
    if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
    outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
    outImage = outImage.rgbSwapped()
    self.img_label.setPixmap(QPixmap.fromImage(outImage))
    self.img_label.setScaledContents(True)


  def submitRegistration(self):

    # PROCEED BUTTON IS CLICKED 
    # stopping the webcam

    self.logic = 3


    name = self.name_input.text()
    roll = self.roll_input.text()
    # combo box theke dept course no input 
    
    

    if (name and roll):
        
        # jana dorkar choose korse naki capture korse ? either way self.captured True kore disi ##########################################
        if (self.captured == True ):
          
          # print(name ,roll, dept, course_no)

          ####################### put the roll dept course no and img to DB
          conn = sqlite3.connect("Attendance_System.db")
          cc = conn.cursor()

          # FOLDER E CURRENT ROLL ER JOTO GULA IMAGE ASE SHEGULAR LIST

          list_of_name_of_images_to_be_saved_in_db = [x for x in os.listdir('root/images/') if self.roll in x]

          for item in list_of_name_of_images_to_be_saved_in_db:
            print('filename: ' + item)
            jj = item
            with open( str( 'root/images/' + jj ) , 'rb') as f:
              Img = f.read()

            data = [(roll,Img),
            ]
          
          #  cc.executemany("INSERT INTO Student VALUES (?,?,?,?)", data)

          conn.commit()
          conn.close()

          # self.chosen_images_dir_list  ETAR CONTENT GULA STUDENT ER NAME E RENAME KORE root/images PATH E COPY/MOVE KORTE HOBE -> DONE check choose existing img function

          #print('[LOG] student '+ name + ' ' + roll + ' '+ ' saved to DB successfully' )
          self.number_of_img_captured = 0

          ####################### done putting the name roll email dept to database 

          msg = QMessageBox()
          msg.setIcon(QMessageBox.Information)
          # msg.styleSheet

          msg.setText('Registration successful' )
          # msg.setInformativeText("This is additional information")
          msg.setWindowTitle("Success")
          # msg.setDetailedText("The details are as follows:")
          msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
          # msg.buttonClicked.connect(msgbtn)
	
          retval = msg.exec_()
          self.img_label.setText("")


        else:
          self.registerstudents_err_label.setText("Please Capture Image ")

    ############# GET BACK TO DASHBOARD

    # if ( self.captured == True ) :
    
    #    self.captured = False
    #    self.mainappwindow = MainAppWindow( self.user )

    #    widget.addWidget(self.mainappwindow)
    #    widget.setFixedSize(770,570)
    #    widget.setCurrentIndex(widget.currentIndex()+1)
    #    print('[LOG] ' +self.u['email'] + ' got back to the dashboard successfully' )
    # else:
    #    self.registerstudents_err_label.setText("Please Capture Image now ")

    
        # EKTA REG DONE KOREI DASHBOARD E FEROT JAITE CHAILE
        # self.captured = False
        # self.mainappwindow = MainAppWindow( "admin" )

        # widget.addWidget(self.mainappwindow)
        # widget.setFixedSize(770,570)
        # widget.setCurrentIndex(widget.currentIndex()+1)
        # print('[LOG] admin got back to the dashboard successfully' )

        #################################################

        # ONEK GULA REG EKBARE KORTE CHAILE 
        self.captured = False
        # self.mainappwindow = MainAppWindow( self.user )

        # widget.addWidget(self.mainappwindow)
        # widget.setFixedSize(770,570)
        # widget.setCurrentIndex(widget.currentIndex()+1)
        # print('[LOG] ' +self.user['email'] + ' got back to the dashboard successfully' )
        

  def gobacktodashboard(self):
  
    adminDashboard = AdminDashboard()

    widget.addWidget(adminDashboard)
    widget.setFixedSize(770,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

    print('[LOG] admin got back to the dashboard successfully' )

class SetCourse(QMainWindow):
    def __init__(self):
        super(SetCourse,self).__init__()
        loadUi('UI/setcourse.ui',self)

        print("[LOG] admin is setting course...")

        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()

        # cc.execute("DROP TABLE Course_Alloc")
        cc.execute("""
              CREATE TABLE IF NOT EXISTS Course_Alloc (
                email text,
                course_no text,
                dept text
              )
              """)
        # SHOBGULA MAIL ER EKTA LIST BANANO LAGBE, DEPARTMENT WISE GROUP KORA OBOSTHAY 
        self.list_of_all_mail = []

        self.selected_dept = ""
        self.selected_teacher = ""
        self.selected_course_no = ""

        # NAME OF ALL DEPTS AVAILABLE IN DB
        dept_list = []

        # ALL DEPARTMENT DB THEKE FETCH
        cc.execute("SELECT dept FROM Course")
        bbx1 = cc.fetchall()
        box1=[]
        # UNIQUE DEPT NAMES
        for i in bbx1:
            if i not in box1:
                box1.append(i)
                dept_list.append(i[0])

        conn.commit()
        conn.close()
        # print(box1, dept_list)

        self.dept_cbox.clear()
        self.teacher_cbox.clear()
        self.course_cbox.clear()
        
        #  REQUIRED  teacher mail fetch from all dept using dept_list
        self.fetch_second_cbox_data(dept_list)

        # makes a dict of { DEPT : LIST OF MAIL OF ALL CORRESPONDING TEACHERS }
        zipped = dict(zip( dept_list,self.list_of_all_mail) )
        # print(zipped) 

        self.dept_cbox.addItem("Click to Select")
        for item in zipped:
            # I.E. CSE : CSE ER SHOBAR MAIL SEPARATED BY COMMA 
            self.dept_cbox.addItem(item, zipped[item])  
            # print( item, zipped[item])

        self.dept_cbox.currentIndexChanged.connect(self.updateDepartmentCombo)
        self.teacher_cbox.currentIndexChanged.connect(self.updateSecondCombo)
        self.course_cbox.currentIndexChanged.connect(self.updateThirdCombo)

        self.updateDepartmentCombo(self.dept_cbox.currentIndex())  # ei func e current idx pathaitesi of states

        self.backtodashboard_btn.clicked.connect( self.gobacktodashboard )
        self.delete_btn.clicked.connect( self.delete_selected_info )
        self.delete_all_btn.clicked.connect( self.delete_all_info )
        self.confirm_btn.clicked.connect( self.save_selected_info )

    def delete_all_info(self):

        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        ##### QMESSAGEBOX SURE YOU WANT TO DO THIS ?????????????
        cc.execute("DELETE FROM Course_Alloc" ) 
        conn.commit()
        conn.close()

        print("[LOG] deleted all rows from course alloc")
        self.confirm_info.setText("Deleted All!")

    def delete_selected_info(self):
        self.teacher_cbox.clear()
        # ENTRIES WILL BE DELETED BASED ON COURSE NO
        self.selected_course_no = self.course_cbox.currentText()

        if( self.selected_course_no!="" ):

          # save to db
          conn = sqlite3.connect("Attendance_System.db")
          cc = conn.cursor()

          dta = [self.selected_course_no]

          # cc.execute("DELETE FROM Course WHERE course_no=?", dta)

          cc.execute("DELETE FROM Course_Alloc WHERE course_no=?", dta)

          print("[LOG] deleted specific row(s)")
          self.confirm_info.setText("Deleted!", dta)

          conn.commit()
          conn.close()

          self.updateDepartmentCombo(self.dept_cbox.currentIndex())

    def save_selected_info(self):
      # SELECTING DATA FROM CBOX
      self.selected_dept= self.dept_cbox.currentText()
      self.selected_course_no = self.course_cbox.currentText()
      self.selected_teacher = self.teacher_cbox.currentText()

      print('[LOG] selected->', self.selected_dept, self.selected_teacher, self.selected_course_no   ) 

      if( self.selected_dept!="" and self.selected_dept!="Click to Select" and self.selected_course_no!="" and self.selected_teacher!=""):

        # save to db
        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()

        # ALREADY ENROLLED COURSE GULA JANTE CHAI
        cc.execute("SELECT * FROM Course_Alloc")
        all_rec = cc.fetchall() 

        xz=1
        
        data = (self.selected_teacher,self.selected_course_no, self.selected_dept)

        for item in all_rec:
            if(item[0]==data[0] and item[1]==data[1] and item[2]==data[2]):
                # MATCH FOUND
                print("[LOG] selected data already in db")
                self.confirm_info.setText("Already Saved")
                xz=0
        
        if(xz==1):
            cc.execute("INSERT INTO Course_Alloc VALUES (?,?,?)", data)

        # show from db
        cc.execute("SELECT * FROM Course_Alloc")
        var = cc.fetchall()
        print('[LOG] showing all from course alloc table')
        for item in var:
            data = item
            print(data[0]+" "+data[1]+" "+data[2])

        conn.commit()
        conn.close()
        # update label 
        self.confirm_info.setText("Success!")
        print("[LOG] success saving data")
      else:
          self.confirm_info.setText("error saving data")
          print("[LOG] error saving data")

    def show_selected_info(self):
        self.selected_dept= self.dept_cbox.currentText()
        self.selected_course_no = self.course_cbox.currentText()
        self.selected_teacher = self.teacher_cbox.currentText()

        if( self.selected_dept!="" and self.selected_course_no!="" and self.selected_teacher!=""):
            print("[LOG] selected", self.selected_dept, self.selected_course_no, self.selected_teacher)
        else:
          self.confirm_info.setText("error fetching data")

    def updateSecondCombo(self):
        self.selected_dept= self.dept_cbox.currentText()
        self.selected_course_no = self.course_cbox.currentText()
        self.selected_teacher = self.teacher_cbox.currentText()

    def updateThirdCombo(self):
        self.selected_dept= self.dept_cbox.currentText()
        self.selected_course_no = self.course_cbox.currentText()
        self.selected_teacher = self.teacher_cbox.currentText()
        
    def fetch_second_cbox_data(self, dept_list ):
        # print(dept_list, type(dept_list[1]))
        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        # for each department bring all mails
        for item in dept_list:
            cc.execute("SELECT email FROM Teacher WHERE dept=?", [item] ) 
            bbx2 = cc.fetchall()
            box2=[]
            teacher_mail_list = []
            for i in bbx2:
                        if i not in box2:
                            box2.append(i)
                            teacher_mail_list.append(i[0])

            self.list_of_all_mail.append(teacher_mail_list)
                
        # print(self.list_of_all_mail) 

        conn.commit()
        conn.close()

    def updateDepartmentCombo(self, index1):
        self.teacher_cbox.clear()
        self.course_cbox.clear()
        # itemData hocche self.dept_cbox.addItem(item, zipped[item]) ei line er zipped[item] ei part ta k indicate kortese
        # ar itemText normally jei item ta select kore asi tar text ta means 
        # self.dept_cbox.addItem(item, zipped[item]) ei line er item ei part ta k indicate kortese
        # EXAMPLE : item = CSE and zipped[item] = ['steve@gmail.com','jobs@gmail.com','bill@gmail.com']
        data_selected_in_dept_cbox = self.dept_cbox.itemData(index1)
        # data_selected_in_dept_cbox e respective dept er teacher mail er ekta list ashbe
        Deptt = self.dept_cbox.itemText(index1)
        
        #  SELECTED Deptt ER J J COURSE CODE DB TE ALREADY ASE OIGULAR EKTA LIST 
        list_course_code = []
        

        # COURSE CODE DB THEKE FETCH USING DEPT from cbox
        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        cc.execute("SELECT course_no FROM Course WHERE dept=?", [Deptt] )
        bbx3 = cc.fetchall()
        box3=[]
        
        for i in bbx3:
            if i not in box3:
                box3.append(i)
                list_course_code.append(i[0])
              
                
        list_ultimate = list_course_code
        

        conn.commit()
        conn.close()

        # data_selected_in_dept_cbox e respective dept er teacher mail er ekta list ashbe
        # EXAMPLE : item = CSE and zipped[item] = ['steve@gmail.com','jobs@gmail.com','bill@gmail.com']
        # so data_selected_in_dept_cbox = ['steve@gmail.com','jobs@gmail.com','bill@gmail.com']
        if data_selected_in_dept_cbox :
            self.teacher_cbox.addItems( data_selected_in_dept_cbox )
            self.course_cbox.addItems(list_ultimate)

        self.selected_dept= self.dept_cbox.currentText()
        self.selected_course_no = self.course_cbox.currentText()
        self.selected_teacher = self.teacher_cbox.currentText()

    def confirm_to_save_data(self):
      self.show_selected_info()

    def gobacktodashboard(self):
  
      adminDashboard = AdminDashboard()

      widget.addWidget(adminDashboard)
      widget.setFixedSize(770,570)
      widget.setCurrentIndex(widget.currentIndex()+1)

      print('[LOG] admin got back to the dashboard successfully' )


class AddCourse(QMainWindow):
  def __init__(self):
    super(AddCourse,self).__init__()
    loadUi('UI/addcourse.ui',self)

    self.backtodashboard_btn.clicked.connect( self.gobacktodashboard )
    self.add_course_btn.clicked.connect( self.goto_add_course )
    #self.update_btn.clicked.connect( self.updates )
    self.delete_course_btn.clicked.connect( self.goto_delete_course )

    # REQUIRED EI DUITA LINE EDIT ER JONNO
    self.dept = ""
    self.course_no = ""

    # REQUIRED EI DUITA CBOX THEKE SELECT ER JONNO
    self.selected_course_no = ""
    self.selected_dept = ""

    # NAME OF ALL DEPTS AVAILABLE IN DB
    dept_list = []

    conn = sqlite3.connect("Attendance_System.db")
    cc = conn.cursor()

    # ALL DEPARTMENT DB THEKE FETCH
    cc.execute("SELECT dept FROM Course")
    bbx1 = cc.fetchall()
    box1=[]
    # UNIQUE DEPT NAMES
    for i in bbx1:
            if i not in box1:
                box1.append(i)
                dept_list.append(i[0])

    # print(box1, dept_list)

    self.dept_cbox.clear()
    self.course_cbox.clear()

    conn.commit()
    conn.close()

    self.dept_cbox.addItem("Click to Select")
    self.dept_cbox.addItems(dept_list)

    # TOKEN2

    self.dept_cbox.currentIndexChanged.connect(self.updateDepartmentCombo)
    self.course_cbox.currentIndexChanged.connect(self.updateCourseCombo)
    print(self.selected_dept)
    print(self.selected_course_no)
    
    self.dep=self.update_text_dept.text()
    
    self.courseno = self.update_text_courseno.text()

    print(self.courseno)
    print(self.dep)
    
    self.update_btn_2.clicked.connect( self.update_course_no )
    self.update_btn_3.clicked.connect(self.update_dept)


  def update_dept(self):
    conn = sqlite3.connect("Attendance_System.db")

    cc = conn.cursor()

    str1 = self.dept_cbox.currentText()
    
    str4 = self.update_text_dept.text()

    print(str1+" "+str4)

    data1 = [(str4)]

    cc.execute("UPDATE Course SET dept = ? WHERE dept = ?", (str4,str1))

    

    data2 = [(str1)]
    conn.commit()
    conn.close()


      

  def update_course_no(self):
    

    conn = sqlite3.connect("Attendance_System.db")

    cc = conn.cursor()

    str1 = self.course_cbox.currentText()
    
    str4 = self.update_text_courseno.text()

    print(str1+" "+str4)

    data1 = [(str4)]

    data2 = [(str1)]



    cc.execute("UPDATE Atten SET course_no = ? WHERE course_no = ?", (str4,str1))
    cc.execute("UPDATE Course_Alloc SET course_no = ? WHERE course_no = ?", (str4,str1))
    cc.execute("UPDATE Course SET course_no = ? WHERE course_no = ?", (str4,str1))
    cc.execute("UPDATE Student SET course_no = ? WHERE course_no = ?", (str4,str1))



    



    


    conn.commit()
    conn.close()



  #def updates(self):
    


    
    


  def goto_delete_course(self):
        
        print(self.selected_course_no)
        conn = sqlite3.connect("Attendance_System.db")
        xx = len(self.selected_course_no)
        str = self.selected_course_no
        course_no = self.selected_course_no
      
        idx = 0
        yy = 0
        
        print(course_no)
         
        data22 = [(course_no)]

        cc = conn.cursor()
        cc.execute("DELETE FROM Course WHERE course_no=?", data22)
        #cc.execute("DELETE FROM Course_Alloc WHERE course_no=?", [self.selected_course_no] )
        conn.commit()
        conn.close()

        self.add_course_info.setText("Deleted!")
        print('[LOG] deleted one course!')  

  def updateDepartmentCombo(self, index1):
      
      self.add_course_info.setText("")
      self.course_cbox.clear()
      Deptt = self.dept_cbox.itemText(index1)
      
      if( Deptt!="Click to Select"):
        self.selected_dept = Deptt
        
        #  SELECTED Deptt ER J J COURSE CODE DB TE ALREADY ASE OIGULAR EKTA LIST 
        list_course_code = []
        

        # COURSE CODE DB THEKE FETCH USING DEPT from cbox
        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        cc.execute("SELECT course_no FROM Course WHERE dept=?", [Deptt] )
        bbx3 = cc.fetchall()

        

        box3=[]
        
        for i in bbx3:
            if i not in box3:
                box3.append(i)
                list_course_code.append(i[0])
                
        list_ultimate = list_course_code
        


        

        conn.commit()
        conn.close()

        # data_selected_in_dept_cbox e respective dept er teacher mail er ekta list ashbe
        # EXAMPLE : item = CSE and zipped[item] = ['steve@gmail.com','jobs@gmail.com','bill@gmail.com']
        # so data_selected_in_dept_cbox = ['steve@gmail.com','jobs@gmail.com','bill@gmail.com']
        if list_course_code :
            self.course_cbox.addItems(list_ultimate)

        self.selected_course_no = self.course_cbox.currentText()
      else :
        self.add_course_info.setText("Choose Department and Course no. to Delete")
        print('[LOG] error choosing dept')  

  def updateCourseCombo(self):
        self.selected_course_no = self.course_cbox.currentText()
        self.update_text_dept.setText(self.selected_dept)
      
      
        self.update_text_courseno.setText(self.selected_course_no)
      

  def goto_add_course(self):
    self.course_no = self.coursecode_input.text() 
    self.dept = self.dept_input.text()    

    if( self.course_no!="" and self.dept!="" ):
      # print(self.course_no,self.dept, 'step 1')
      self.adding_course()
    else:
      self.add_course_info.setText("Enter both Department and Course no. correctly")
      print('[LOG] error getting data')  

  def adding_course(self):
    if( len(self.course_no)!=4  ): 
      self.add_course_info.setText("Enter Course no. in 4 digits ")
      print('[LOG] error getting correct data')  
    elif( len(self.dept)!=3 ): 
      self.add_course_info.setText("Enter Department name in 3 letters")
      print('[LOG] error getting correct data') 
    elif( len(self.course_no)==4 and ( len(self.dept)==3 or len(self.dept)==2 ) and self.course_title_input.text()!=""):  

      # print(self.course_no,self.dept, 'step 2' )

      conn = sqlite3.connect("Attendance_System.db")
      cc = conn.cursor()
      # cc.execute("DROP TABLE Course")
      cc.execute("""
          CREATE TABLE IF NOT EXISTS Course (
              course_no text,
              dept text
      )
      """)
      
      cc.execute("SELECT * FROM Course")

      all_data_from_db = cc.fetchall()
      data_from_cbox = (self.course_no,self.dept)

      xx=1

      # db er shathe selected data match kora thakle ar db te entry hobe na same data 
      for item in all_data_from_db:
        if(item[0]==data_from_cbox[0] and item[1]==data_from_cbox[1]):
            xx=0

      

      course_title = self.course_title_input.text()

      self.course_no = self.dept + self.course_no+ "-" +course_title
    
      data = (self.course_no,self.dept)
      
      if(xx==1):
          cc.execute("INSERT INTO Course VALUES (?,?)", data)
          self.add_course_info.setText("Entry Successful")
          print('[LOG] Entry Successful' , self.course_no, self.dept )
      elif(xx==0):
          self.add_course_info.setText("Already Added")
          print('[LOG] already added' , self.course_no, self.dept )
      
  
      conn.commit()
      conn.close()


      ###################################################################
      #  show all the courses from course table with course number
      #############################################################

      # conn = sqlite3.connect("Attendance_System.db")
      # cc = conn.cursor()

      # cc.execute("SELECT * FROM Course")
      # var = cc.fetchall()

      # for item in var:
      #     data = item
      #     print(data[0]+" "+data[1])

      # conn.commit()
      # conn.close()

    else:
      self.add_course_info.setText("error connecting db")
      print('[LOG] error connecting db') 

    # UPDATING THE NEWLY ADDDED COURSE TO THE NEARBY CBOX
    # FORCING USER TO SELECT THE DEPT AGAIN

    # DO IT MAN

    

  def gobacktodashboard(self):
  
    adminDashboard = AdminDashboard()

    widget.addWidget(adminDashboard)
    widget.setFixedSize(770,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

    print('[LOG] admin got back to the dashboard successfully' )

class AdminDashboard(QMainWindow):
  def __init__(self):
    super(AdminDashboard,self).__init__()
    loadUi('UI/admindashboard.ui',self)
    
    self.u = 'admin'
    self.logout_btn.clicked.connect( self.logout )
    self.registerstudents_btn.clicked.connect( self.gotoregisterstudents )
    self.addcourse_btn.clicked.connect( self.gotoaddcourse )
    self.setcourse_btn.clicked.connect( self.gotosetcourse )
    self.delete_all_btn.clicked.connect( self.gotodeleteall )

  def gotodeleteall(self):

        conn = sqlite3.connect("Attendance_System.db")
        cc = conn.cursor()
        cc.execute("DELETE FROM Student" ) 
        conn.commit()
        conn.close()

        print('[LOG] Deleted all from student table')

  def gotosetcourse(self):

    setCourse = SetCourse()
    widget.addWidget(setCourse)
    widget.setFixedSize(770,570)
    widget.setCurrentIndex(widget.currentIndex()+1)
  
  def gotoaddcourse(self):

    addCourse = AddCourse()
    widget.addWidget(addCourse)
    widget.setFixedSize(770,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

  def gotoregisterstudents(self):

    registerStudents = RegisterStudentsViaAdmin(self.u)
    widget.addWidget(registerStudents)
    widget.setFixedSize(780,590)
    widget.setCurrentIndex(widget.currentIndex()+1)

  
  def logout_confirmation(self, i):

    # if OK button is clicked then logout
    if ( i.text() == "OK" ):
  
      login = Login()
      widget.addWidget(login)
      widget.setFixedSize(470,570)
      widget.setCurrentIndex(widget.currentIndex()+1)
      print('[LOG] admin logged out')

  def logout(self):
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText('Are you sure to Logout?')
    msg.setWindowTitle("Logout Confirmation")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.setDefaultButton(QMessageBox.Cancel)
    msg.buttonClicked.connect(self.logout_confirmation)
	
    retval = msg.exec_()
  
class AdminLogin(QMainWindow):
  def __init__(self):
    super(AdminLogin,self).__init__()
    loadUi('UI/adminlogin.ui',self)

    
    self.fixedEmail = "systemproject3200@gmail.com"
    self.login_btn.clicked.connect(self.adminLogin)
    self.change_pass_btn.clicked.connect(self.change_pass)
    self.backtologin_btn.clicked.connect( self.backtologinFunction )

  def backtologinFunction(self):
      login = Login()
      widget.addWidget(login)
      widget.setFixedSize(470,570)
      widget.setCurrentIndex(widget.currentIndex()+1)

  def gotoAdminDashboard(self):
      adminDashboard = AdminDashboard()
      widget.addWidget(adminDashboard)
      widget.setFixedSize(770,570)
      widget.setCurrentIndex(widget.currentIndex()+1)

  def adminLogin(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if( email!="" and email==self.fixedEmail and password!="" ):

            try:
                user = fba.authentication.sign_in_with_email_and_password(email, password)
                print('[LOG] admin log in successful ')
                self.gotoAdminDashboard()

            except requests.exceptions.HTTPError as e:
              # https://stackoverflow.com/questions/61488376/firebase-error-handling-for-account-creation-and-login-pyrebase
              import json
              error_json = e.args[1]
              error = json.loads(error_json)['error']['message']
              if error == "EMAIL_NOT_FOUND":
                  print("[LOG] email not found in pyrebase") 
                  self.login_info.setText('Email not found')
              elif( error == "INVALID_PASSWORD" ): 
                  print("[LOG] invalid password") 
                  self.login_info.setText('Please enter correct password')
              else :
                print(error)
     
        else:
          self.login_info.setText('Please Enter Email & Password correctly')
          print('[LOG] admin login unsuccessful' )
  
  def change_pass(self):

    emailid = self.email_input.text()

    if( emailid!="" and emailid==self.fixedEmail):
        fba.authentication.send_password_reset_email(self.fixedEmail)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Please Check your email {}'.format(self.fixedEmail) )
        msg.setWindowTitle("Enter Email")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()      
        self.login_info.setText('')
      
    else:
        self.login_info.setText('Enter Admin Email & click Change Password again')


class Login(QMainWindow):
  def __init__(self):
    super(Login,self).__init__()
    loadUi('UI/login.ui',self)

    # self.mainappwindow = MainAppWindow()
    # widget.addWidget(self.mainappwindow)
    # widget.setCurrentIndex(widget.currentIndex()+1)
    
    self.submit_btn.clicked.connect(self.loginFunction)
    self.admin_btn.clicked.connect(self.goToAdminLogin )
    self.register_btn.clicked.connect( self.goToSignUp )
    self.forgot_pass_btn.clicked.connect( self.forgot_pass )

  # def passingInfo(self):
  #   self.mainappwindow.welcome_label.setText(user['email'])

  def goToAdminLogin(self):
    AdminLoginWindow = AdminLogin()
    widget.addWidget(AdminLoginWindow)
    #  CHANGE THE SIZE OF THE MAIN WINDOW
    widget.setFixedSize(470,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

  def forgot_pass(self):

    emailid = self.email_input.text()

    if( emailid!=""):
        fba.authentication.send_password_reset_email(emailid)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
          # msg.styleSheet
        msg.setText('Please Check your email {}'.format(emailid) )
          # msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Enter Email")
          # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
          # msg.buttonClicked.connect(msgbtn)
        retval = msg.exec_()
      
        self.login_info.setText('')
      
    else:
        self.login_info.setText('Enter Email & click Forgot Password again')

  def goToSignUp(self):
    SignUpWindow = SignUp()
    widget.addWidget(SignUpWindow)
    #  CHANGE THE SIZE OF THE MAIN WINDOW
    widget.setFixedSize(540,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

  def gotomainapp(self,user):
  
    print( '[LOG] ' + user['email'] + ' trying to login ' )
  
    self.mainappwindow = MainAppWindow(user)
    # self.mainappwindow.welcome_label.setText(user['email'])
    widget.addWidget(self.mainappwindow)
    widget.setFixedSize(770,570)
    widget.setCurrentIndex(widget.currentIndex()+1)

  def loginFunction(self):
    email = self.email_input.text()
    password = self.password_input.text()

    if( email and password ):
      try:
          user = fba.authentication.sign_in_with_email_and_password(email, password)
          # before 1 hour (?)
          # user = fba.authentication.refresh( user['refreshToken'] )

          user_idtoken = user['idToken']
          # x = fba.authentication.get_account_info(user_idtoken)
          
          print('[LOG] login successful ')
          self.gotomainapp(user)

      except requests.exceptions.HTTPError as e:
        # https://stackoverflow.com/questions/61488376/firebase-error-handling-for-account-creation-and-login-pyrebase
        import json
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error == "EMAIL_NOT_FOUND":
            print("[LOG] email not found in pyrebase") 
            self.login_info.setText('Email not found')
        elif( error == "INVALID_PASSWORD" ): 
            print("[LOG] invalid password") 
            self.login_info.setText('Please enter correct password')
        else :
          print(error)

    else:
      self.login_info.setText('Please Enter both Email & Password')
      print('[LOG] login unsuccessful' )

class SignUp(QMainWindow):
  def __init__(self):
    super(SignUp,self).__init__()
    loadUi('UI/registersignup.ui',self)

    self.signupbtn.clicked.connect( self.Signup )
    self.backtologin_btn.clicked.connect( self.backtologinFunction )

    conn = sqlite3.connect("Attendance_System.db")
    cc = conn.cursor()

    dept_list = []

        # ALL DEPARTMENT DB THEKE FETCH
    cc.execute("SELECT dept FROM Course")
    bbx1 = cc.fetchall()
    box1=[]
        # UNIQUE DEPT NAMES
    for i in bbx1:
            if i not in box1:
                box1.append(i)
                dept_list.append(i[0])
                
    conn.commit()
    conn.close()

    self.dept_cbox.addItem('Click to select')
    self.dept_cbox.addItems(dept_list)

  def Signup(self):

    namesignup = self.name_input.text()
    deptsignup = self.dept_cbox.currentText()
    emailsignup = self.signupemail_input.text()
    passwordsignup = self.signuppassword_input.text()
    confirmpassword = self.signupconfirmpassword_input.text()
    

    if( namesignup and deptsignup and  emailsignup and ( passwordsignup == confirmpassword ) ):
        
        passwordsignup = self.signuppassword_input.text()
        try:

          # ################## PYREBASE ##########################
          user = fba.authentication.create_user_with_email_and_password(emailsignup,passwordsignup)
          print('[LOG] successfully created user with ' + user['email'] )
          # ################## PYREBASE ##########################

          # ################## DB ##########################
          
          conn = sqlite3.connect("Attendance_System.db")
          cc = conn.cursor()
          # cc.execute("DROP TABLE Teacher")
          cc.execute("""
                CREATE TABLE IF NOT EXISTS Teacher (
                email text,
                password text,
                name text,
                dept text
          )""")

          
          #EIKHANEASHO
          hashed_pass = passwordsignup

          data = [(emailsignup,hashed_pass,namesignup,deptsignup,),]

          cc.executemany("INSERT INTO Teacher VALUES (?,?,?,?)", data)

          # cc.execute("SELECT * FROM Teacher")
          # var = cc.fetchall()

          # for item in var:
          #     data = item
          #     print(data[0]+" "+data[1]+" "+data[2]+" "+data[3])

          conn.commit()
          conn.close()

          # ################## DB ##########################

          msg = QMessageBox()
          msg.setIcon(QMessageBox.Information)
          msg.setText('account created with '+ user['email'] + ' successfully' )
          msg.setWindowTitle("Success")
          msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
          msg.setDefaultButton(QMessageBox.Ok)
          retval = msg.exec_()

          login = Login()
          widget.addWidget(login)
          widget.setFixedSize(470,570)
          widget.setCurrentIndex(widget.currentIndex()+1)

        except requests.exceptions.HTTPError as e:
            import json
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == "EMAIL_EXISTS":
                print("[LOG] email already found in pyrebase") 
                self.signup_info.setText('Already Registered, try a new Email')
            elif( error == "WEAK_PASSWORD" ): 
                print("[LOG] weak password") 
                self.login_info.setText('Password should be at least 6 characters')
            else :
                print(error)
        else:
            self.signup_info.setText('Please Enter required fields correctly!')

  def backtologinFunction(self):
      login = Login()
      widget.addWidget(login)
      widget.setFixedSize(470,570)
      widget.setCurrentIndex(widget.currentIndex()+1)

# main
app = QApplication(sys.argv)
mainWindow = Login()

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)

# widget.setWindowTitle('Login') # do this for al lthe other windows ???????????
widget.setWindowTitle('') # do this for al lthe other windows ???????????
widget.setFixedSize(470,570)
# widget.setMinimumSize(470,570) # w,h
# widget.setMaximumSize(600,900) # w,h
widget.show()

try:
  sys.exit(app.exec_())
except :
  print("[LOG] Exiting the app... ")

#kajkorseshob-blink_kaj_kore_final