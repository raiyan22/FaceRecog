import pyrebase

firebaseConfig = {
    #
    # 'apiKey': "AIzaSyAnr-o2zCzgzUVk8iqz7-anYIptJsy7hmI",
    # 'authDomain': "authpy03.firebaseapp.com",
    # 'projectId': "authpy03",
    # 'databaseURL': "https://authpy03-default-rtdb.firebaseio.com/",
    # 'storageBucket': "authpy03.appspot.com",
    # 'messagingSenderId': "262707042284",
    # 'appId': "1:262707042284:web:e6fbfc7446629cfa6c92c9"

    'apiKey': "AIzaSyAChJQ95NV1JVeGI74Ol8YI9johj8bGfRk",
    'authDomain': "attendancesystemproject-d957f.firebaseapp.com",
    'projectId': "attendancesystemproject-d957f",
    'databaseURL': "https://attendancesystemproject-d957f-default-rtdb.firebaseio.com/",
    'storageBucket': "attendancesystemproject-d957f.appspot.com",
    'messagingSenderId': "898857801372",
    'appId' : "1:898857801372:web:2a853745600af12fa5ff59"

    }

#  initializing 
firebase = pyrebase.initialize_app(firebaseConfig)
# authentication 
authentication = firebase.auth()  

