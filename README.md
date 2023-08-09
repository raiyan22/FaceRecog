# FaceRecog
An end to end GUI based Application created using Python that facilitates the teacher to take attendance automatically based on the face recognition method.

## Frameworks Used

For Backend
- face_recognition (v1.3.0)
- dlib (v19.22.0) & cmake (v3.18.4)
- opencv (v4.5.1.48)
- pyrebase (v3.0.27)
- sqlite (v3.31.1)
  
For Frontend
- PyQt5 (v5.15.4)
  
👉 [Here](https://drive.google.com/file/d/1-A9H7sTsYedEkvxwlusMXIW2qfoxZ_P8/view?usp=sharing) is a working demo of this project.

## Main Features

- Teacher can take attendance by using facial feature recognition in 
real time and view related information inside the app.
- Upon request from the student, teacher can manually add 
attendance.
- Admin can add, update or delete courses and register new 
students.
- Admin is capable of bulk registration through selecting a csv file.
- Admin can assign courses to teachers in order for the teachers to 
be able to take attendance.
- Admin or Teacher can change their password at any time through 
a link sent to their email

## Database Design
There are six tables in the associated database and the schema diagram is given below

![db](https://github.com/raiyan22/FaceRecog/assets/58294098/d3832963-cfde-4298-85ba-280350eecd50)

## Workflow 

- The teachers will sign up
- Admin will create/delete/update courses for the semester
- Admin will assign courses to corresponding teachers
- Admin will register students with the help of the data in a csv. The students were previously asked to fill in their information into the csv
- Student registration process is very simple. As soon as the csv is uploaded, all the data will be saved into the database
- The students are to provide a single image of their face renamed as *myname.jpg* where *myname* represents his/her actual name and this must be same as the name provided in the csv
- Upon Successful registration the stdents will be assigned for the respective courses by the admin
- The teacher will start taking attendance only after choosing the correct course otherwise the students will be detected as unregistered 
- The students are supposed to show their face in front of the camera mounted in the classroom and they will be automatically marked as attended
- Teacher has the ability to add the attendance manually for a particular student
- Teacher can view the attendance based on a certain date and also can export the attendance information as csv
- Teacher can use the forget password feature in case it is needed

## Flow Diagram

The entire flow of the application is presented in the following diagram

![flow](https://github.com/raiyan22/FaceRecog/assets/58294098/e557f4b0-2e75-4737-a58d-2b5078f83a48)

## Navigation

This image shows the windows that can be explored by the Teacher for various tasks

![navapp](https://github.com/raiyan22/FaceRecog/assets/58294098/407b893c-e1af-4c45-9563-ae250a9ec82f)

Although this application serves the basic purpose and fulfills the objectives, there are scope for further enhancements. 
The resolution of the camera plays a very important role in recognizing the image. 
A device equipped with a good processing speed enabled with a high end graphics processing unit is necessary

For further knowledge, please refer to this [report](https://github.com/raiyan22/FaceRecog/files/12306416/Report.pdf)
