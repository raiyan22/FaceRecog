import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox, QCalendarWidget
from datetime import datetime
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi
from datetime import datetime 

class CalendarDemo(QMainWindow):
    # global currentYear, currentMonth
    
    # currentMonth = datetime.now().month
    # currentYear = datetime.now().year
    global day, mon, yr
    day = datetime.now().day # gives "10"
    mon = datetime.now().month  # gives "6", not "06"
    yr = datetime.now().year # gives "2021"

    def __init__(self):
        super(CalendarDemo,self).__init__()
        loadUi('trypropic.ui',self)
        
        self.cal.setGridVisible(True)
        # print(day, mon, yr)
        # to view a certain date preselected on cal
        self.cal.setSelectedDate(QDate(yr,mon,day))

        # to print selected date from cal to console way 1
        # self.cal.clicked.connect( lambda dateval: print(dateval.toString()) ) # gives Fri Jun 11 2021 
        
        # to print selected date from cal to console way 2
        self.cal.clicked.connect( self.getDate )

    def getDate(self, qDate):
        print('{0}-{1}-{2}'.format(qDate.day(),qDate.month(), qDate.year() ))
        # print( str(qDate.dayOfYear() ))
        # print( str(qDate.dayOfWeek() ))
        
        
app = QApplication(sys.argv)
demo = CalendarDemo()
demo.show()

try:
    sys.exit(app.exec_())
except SystemExit:
    print('Closing Window...')
