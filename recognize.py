import cv2 as cv
import numpy as np
import os
import face_recognition
from datetime import datetime
import csv


def create_new_csv(csv_filename):

    ############################################################################################################
    #  CREATE A NEW CSV AND CLOSE IT WE WILL READ THAT LATER
    ############################################################################################################

    # now = datetime.now()
    # dtString = now.strftime('%d-%m-%Y')
    # courseCode = "CSE-3207"

    # csv_filename = '{}-{}'.format(courseCode,dtString)

    attendance_path = 'C:/Users/Raiyan/Desktop/pyqt5Tutorial/root/Attendance'

    with open(f'{attendance_path}/{csv_filename}.csv', 'w+') as f:
        f.close()

    #############################################################################################################


####################################### MAIN TASK PART 1 ##################################################

courseCode = "CSE-3207"
# path = 'root/images'
path = 'C:/Users/Raiyan/Desktop/pyqt5Tutorial/root/images'
images = []
classNames = []
myList = os.listdir(path)

# print(myList) # names of image files

for cl in myList:
    currentImg = cv.imread(f'{path}/{cl}')
    images.append(currentImg)
    classNames.append(os.path.splitext(cl)[0])
# print(classNames) # names of image files without extension

#########################################################################################


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


def markAttendance(name):

    now = datetime.now()
    dtString = now.strftime('%d-%m-%Y')

    csv_filename = '{}-{}'.format(courseCode, dtString)

    attendance_path = 'C:/Users/Raiyan/Desktop/pyqt5Tutorial/root/Attendance'

    with open(f'{attendance_path}/{csv_filename}.csv', 'r+') as f:

        myDataList = f.readlines()
        namelist = []
        for line in myDataList:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            TIMEString = now.strftime('%I:%M:%S')
            f.writelines(f'\n{name},{TIMEString}')

#############################################################################################################################


encodeListKnown = findEncodings(images)
# print(len(encodeListKnown))
print('Encoding complete')

# cap = cv.VideoCapture("v4.mp4")
cap = cv.VideoCapture(0)

csv_created = False

while True:
    ret, img = cap.read()
    if ret==False:
        print("did not run")
        break
    imgSmall = cv.resize(img,(0,0), None, 0.25, 0.25)
    imgSmall = cv.cvtColor(imgSmall, cv.COLOR_BGR2RGB)

    if (csv_created == False):

        now = datetime.now()
        dtString = now.strftime('%d-%m-%Y')
        courseCode = "CSE-3207"
        csv_filename = '{}-{}'.format(courseCode, dtString)

        create_new_csv(csv_filename)

        csv_created = True

    facesCurrentFrame = face_recognition.face_locations(imgSmall)
    encodesCurrentFrame = face_recognition.face_encodings(
        imgSmall, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(
            encodeListKnown, encodeFace)
        # print(faceDistance) # the lesser the distance the best match it is
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            s_name = classNames[matchIndex]
            name = ''
            print(s_name)

            name = s_name.split('_')[0]

            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
            cv.putText(img, name, (x1+6, y2-6),
                       cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            markAttendance(name)

        else:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
            cv.putText(img, 'Unknown', (x1+6, y2-6),
                       cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            print("notFound")

    cv.imshow("Output", img)
    if cv.waitKey(1) & 0xFF == ord('p'):
        break
cap.release()
cv.destroyAllWindows()
