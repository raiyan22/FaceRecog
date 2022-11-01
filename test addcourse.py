from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog, QComboBox, QTableWidget
from PyQt5.QtCore import QTimer, QTime , Qt, QDate, QDateTime
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.uic import loadUi
import sys
import os 
import sqlite3

conn = sqlite3.connect("Attendance_System.db")
cc = conn.cursor()
cc.execute("DROP TABLE Course")
cc.execute("""
    CREATE TABLE IF NOT EXISTS Course (
        course_no text,
        dept text
    )
    """)
conn.commit()
conn.close()

class AddCourse(QMainWindow):
  def __init__(self):
    super(AddCourse,self).__init__()
    loadUi('UI/addcourse.ui',self)
    
    self.dept = ""
    self.course_no = ""

    self.add_course_btn.clicked.connect( self.goto_add_course )

  def goto_add_course(self):
    self.course_no = self.coursecode_input.text() 
    self.course_no = self.dept_input.text() 

    if( self.course_no!="" and self.dept!="" ):
      print(self.course_no,self.dept, 'go to add course')
      self.adding_course()
    else:
      self.add_course_info.setText("enter correctly")
      print('[LOG] error getting data')
      

  def adding_course(self):
    if(self.dept and self.course_no ): 

      print(self.course_no,self.dept, 'adding course')
      
      # conn = sqlite3.connect("Attendance_System.db")
      # cc = conn.cursor()

      # data = [(self.course_no,self.dept),]
      
      # cc.executemany("INSERT INTO Course VALUES (?,?)", data)
      # conn.commit()
      # conn.close()

      #######################
      #  show 
      #######################

      # conn = sqlite3.connect("Attendance_System.db")
      # cc = conn.cursor()

      # cc.execute("SELECT * FROM Course")
      # var = cc.fetchall()

      # for item in var:
      #     data = item
      #     print(data[0]+" "+data[1])
      #     print("\n")

      # conn.commit()
      # conn.close()
    else:
      print('select department and course no')
      

  def on_combobox_dept_text_change_func(self, dept):
      self.dept = dept

#################################################################################################################   

app = QApplication(sys.argv)
mainWindow = AddCourse()

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)

# widget.setWindowTitle('Login') # do this for al lthe other windows ???????????
widget.setWindowTitle(' ') # do this for al lthe other windows ???????????
widget.setFixedSize(770,570)
# widget.setMinimumSize(470,570) # w,h
# widget.setMaximumSize(600,900) # w,h
widget.show()

try:
  sys.exit(app.exec_())
except :
  print("[LOG] Exiting ... ")
  


