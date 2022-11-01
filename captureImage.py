
def extract_username_from_email():
     x = input("enter : ")
     # print(x)
     # getting rid of leading + trailing spaces
     # x = x.strip() 
     x = x[ : x.find("@")  ].strip()

     print(x)


'''
might come handy :)

f=open("file")
for line in f:
    words= line.split()
    if "@" in words:
       print "@"+words.split("@")[-1]
f.close()
'''

import cv2 as cv
import os
import firebaseAuth as fba 

cam = cv.VideoCapture(0)

# Path = 'C:/Users/Raiyan/Desktop/pyqt5Tutorial/root/mages'

Path = 'root/Images'

while True:
  success , frame = cam.read()

  if not success:
    print('something is wrong')

  cv.imshow('test',frame)
  k = cv.waitKey(1)

  if   k%256 == ord('p'):
    break

  elif k%256 == ord('m'):

    img_name = 'username.png'
    

    # x = cv.imwrite(img_name,frame)
    cv.imwrite(os.path.join(Path , img_name ),frame)
    print('captured success')

    # if os.path.exists("username.png"):
    #   os.remove("username.png")
    # else:
    #   print("The file does not exist")


cam.release()

