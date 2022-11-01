'''
issue 1
in __init__
    self.database_url = config["databaseURL"]
KeyError: 'databaseURL'

first created a realtime db in firebase thru browser
then had a db url from firebase site then 
solved it using

https://firebase.google.com/docs/database/web/start?authuser=0
'''


'''
Installing collected packages: httplib2, requests, oauth2client, jws, googleapis-common-protos, requests-toolbelt, python-jwt, pycryptodome, gcloud, pyrebase
  Attempting uninstall: requests
    Found existing installation: requests 2.25.1
    Uninstalling requests-2.25.1:
      Successfully uninstalled requests-2.25.1
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
tensorboard 2.4.1 requires requests<3,>=2.21.0, but you have requests 2.11.1 which is incompatible.
Successfully installed gcloud-0.17.0 googleapis-common-protos-1.52.0 httplib2-0.18.1 jws-0.1.3 oauth2client-3.0.0 pycryptodome-3.4.3 pyrebase-3.0.27 python-jwt-2.0.1 requests-2.11.1 requests-toolbelt-0.7.0
'''

import pyrebase

firebaseConfig = {

    # 'apiKey': "AIzaSyDhJWquVVNntgfU8iH6at-aILYeBnD-W94",
    # 'authDomain': "authpyy.firebaseapp.com",

    # 'databaseURL':"https://authpyy-default-rtdb.firebaseio.com/",  ### WTF !! Go see at top issue 1 

    # 'projectId': "authpyy",
    # 'storageBucket': "authpyy.appspot.com",
    # 'messagingSenderId': "351216534712",
    # 'appId': "1:351216534712:web:8b3ba8593ad8d27e88e04d",
    # 'measurementId': "G-W7H9CQZK0Y"

    # 2nd time 
    # 'apiKey': "AIzaSyANMYzMv1w6twV264yWbqUtBPxVbtulOuk",
    # 'authDomain': "authv2-a4997.firebaseapp.com",

    # 'databaseURL': "https://authv2-a4997-default-rtdb.firebaseio.com/",
  
    # 'projectId': "authv2-a4997",
    # 'storageBucket': "authv2-a4997.appspot.com",
    # 'messagingSenderId': "316130484234",
    # 'appId': "1:316130484234:web:95b24f145246535e33fff3"

    #3rd time
    'apiKey': "AIzaSyAnr-o2zCzgzUVk8iqz7-anYIptJsy7hmI",
    'authDomain': "authpy03.firebaseapp.com",
    'projectId': "authpy03",
    'databaseURL': "https://authpy03-default-rtdb.firebaseio.com/",
    'storageBucket': "authpy03.appspot.com",
    'messagingSenderId': "262707042284",
    'appId': "1:262707042284:web:e6fbfc7446629cfa6c92c9"

    # 4th time renewed 8th june
    # 'apiKey': "AIzaSyBolv3dn8My1J68lapPqCFaJ7ZqJutlI9k",
    # 'authDomain': "authpy-b04.firebaseapp.com",
    # 'projectId': "authpy-b04",
    # 'databaseURL': "https://authpy-b04-default-rtdb.firebaseio.com/",
    # 'storageBucket': "authpy-b04.appspot.com",
    # 'messagingSenderId': "510123890543",
    # 'appId': "1:510123890543:web:e7b8e6840b9f7da6e77a9a"

    }

#  initializing 
firebase = pyrebase.initialize_app(firebaseConfig)


authentication = firebase.auth()  # authentication is just a variable here 

def signup():
  # email = 'raiyan@gmail.com'
  # password = 'qwertyLILmega'

  email = str(input('enter a new email : '))
  password = str(input('enter password : '))

  try:
    user = authentication.create_user_with_email_and_password(email,password)
    print('successfully created user')
    # do you want to login ????
  except:
    print('email already exists')


# https://www.youtube.com/watch?v=LaGYxQWYmmc&list=PLs3IFJPw3G9Jwaimh5yTKot1kV5zmzupt&ab_channel=CodeFirst 

# see from 10

def login():
  email = str(input('enter your email : '))
  password = str(input('enter your password : '))

  try: 
    user = authentication.sign_in_with_email_and_password(email, password)

    if user:
      # print(user['email'] + ' logged in hehe :)')
      # print(authentication.get_account_info(user['idToken']))
       print(user['email']+ ' logged in')
       
  except:
      print('invalid email or password')
  x = input('entervalue: ')
  if(x=='o'):
      user = None
      print(user)


# signup()
# login()

def realtimeDb():

    
    db = firebase.database()
    #  PUSH DATA TO DB

    # data = { 
    #         'address' : ['dhaka','bangladesh'],
    #         'email' : 'islam1707022@gmail.com',
    #         'roll' : '1707022',
    #         'name' : 'raiyan'
    #        }
    data = { 
            'address' : ['bangladesh'],
            'email' : 'i@gmail.com',
            'roll' : '172',
            'name' : 'gyhgykkkkhjk'
           }

    
    
    # if we donot write this line then we will get a random KEY there on firebaseDB, upon expanding which we actually see the data structured as a tree
    
    db.child('root').child(data['name']).set(data) 

    # db.push(data)

    # UPDATE DATA
    city = 'london'

    # db.child(data['name']).child('address').update({'address':'cool'})

    ## THIS IS TO REMOVE DATA 
    # db.child(data['name']).child('address').remove({'address':'cool'})
    
    # this is on the cloud 
    # db.child(data['name']).update({'address':[city]})


    #  see from 10:00 of this link
    #  https://www.youtube.com/watch?v=1DhvKCjG2NE&list=PLs3IFJPw3G9Jwaimh5yTKot1kV5zmzupt&index=4&ab_channel=CodeFirst

    
 
    var = db.child('root').get()
    key = ''
    for item in var.each():

      if(item.val()['name']=='gyhgykkkkhjk'):
        key = item.key()
      print(item.val())  
      print(item.val()['roll'])
      print(item.key())  # eta kintu root er theke j child ta ashche oita  root>raiyan(this key)
      print(key)  
    
# realtimeDb()


# storage section e giye cloud storage activate korsi 
# we can upload files here and store it 
# changed the rules there 

# setting up storage

def storeData():
    storage = firebase.storage()

    # upload a file to storage
    name_file_on_cloud = str(input('enter the name of the file (books/fiction/xyz.pdf will create two folders first) : ')) 
    # books/fiction/xyz.pdf will create two folders first 
    name_of_the_file_on_your_local_storage = str(input('enter the directory of the file : ')) 

    storage.child(name_file_on_cloud).put(name_of_the_file_on_your_local_storage)
    
    storage.child()

    # get the url to the file uploaded 

    file_url = storage.child(name_file_on_cloud).get_url(None)
    print(file_url)
    # download the file

    download_url = str(input('enter download url : '))
    # https://firebasestorage.googleapis.com/v0/b/authpyy.appspot.com/o/login.ui?alt=media
    # ei link e gele direct browser theke naame

    # nicher ta diye vscode e namse but download url hishebe input dite hoy the full dir of the file ON THE CLOUD :3
    storage.child(download_url).download('downloaded.pdf')



