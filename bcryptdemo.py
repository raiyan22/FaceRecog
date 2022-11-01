# print ( hash("swat") ) 



import time
import bcrypt
 
actual_password = "thisismypassword"
# actual_password = bytes(actual_password, 'utf-8')  # gives type err if the string is already in bytestring
# actual_password1 = b"thisismypassword"

start = time.time()
# hashed_pass = bcrypt.hashpw( actual_password, bcrypt.gensalt() )
# hashed_pass = bcrypt.hashpw( actual_password, bcrypt.gensalt( rounds = 12 ) )  
# rounds = 12 by default, larger value needs more cpu power + time but more secure  
hashed_pass = bcrypt.hashpw(actual_password.encode('utf8'), bcrypt.gensalt())
print(hashed_pass)
end = time.time()
total_time = end - start

print(hashed_pass)    # gives random string for the same input every **ing time

if bcrypt.checkpw( actual_password.encode('utf8') , hashed_pass ):
  print("accepted")
else: 
  print("nope")

print("hashed within " + format( total_time , '.2f' ) + " seconds" )

