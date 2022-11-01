# try shutil now 

# try measuring time now, each hour 

##############################################################

# try date time

# from datetime import datetime 

# now = datetime.now()
# dtString = now.strftime('%d-%m-%Y')

# courseCode = "CSE-3207"

# csv_filename = '{}-{}'.format(courseCode,dtString)
# # print(dtString)
# print(x)

##############################################################
# x= 'LadyGaga_04.csv'.split('.')[1] 
# print(x)

###########################################################################

#  moving a file to new dir after renaming it 
# import os 

# prevName = 'C:/Users/Raiyan/Desktop/naam ketty.jpg'
# newName = 'C:/Users/Raiyan/Desktop/pyqt5Tutorial/root/images/KatyPerry.jpg'

# os.rename(prevName,newName)

###########################################################################

# import os 

# currentdir = 'root/Attendance'

# for fileitem in os.listdir(currentdir):
#   print(fileitem)
#   fileitem = fileitem.replace(".","-")
#   splitted_file_name = fileitem.split("-")
#   # splitted_file_name = ['CSE', '3207', '24', '3', '2021', 'csv']
#   print( splitted_file_name )

###########################################################################

attendance_path = 'root/Attendance'
csv_filename = 'CSE-3207-25-02-2021'
with open(f'{attendance_path}/{csv_filename}.csv','r') as f:

      myDataList = f.readlines()
      myDataList = [ s.strip() for s in myDataList ] # new line shorailam from each list Items
      myDataList = [ s for s in myDataList if s != ""] # removed the first item cz it is null
      

      print(myDataList)
      # namelist = []
      for line in myDataList:
        entry = line.split(',')
        # namelist.append(entry[0])
        # print(entry[0],entry[1])
        print(entry)
      
      # print(namelist)
        # f.writelines(f'\n{name},{TIMEString}')





