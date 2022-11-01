import sqlite3

conn = sqlite3.connect("Attendance_System.db")
cc = conn.cursor()

# cc.execute("DELETE FROM Course")
    
# cc.execute("DELETE FROM Teacher")
# cc.execute("DELETE FROM Student")
    
# cc.execute("DELETE FROM Course_Alloc")
# cc.execute("DELETE FROM Atten")


    
# cc.execute("DROP TABLE Teacher")
#cc.execute("DROP TABLE Course")
    
#cc.execute("DROP TABLE Course_Alloc")
#cc.execute("DROP TABLE Course_Alloc")
# cc.execute("DROP TABLE Atten")

      # cc.execute("DROP TABLE Course")
# cc.execute("""
#           CREATE TABLE IF NOT EXISTS Course (
#               course_no text,
#               dept text
#       )
#       """)

# cc.execute("""
#               CREATE TABLE IF NOT EXISTS Course_Alloc (
#                 email text,
#                 course_no text,
#                 dept text
#               )
#               """)

# cc.execute("""
#               CREATE TABLE IF NOT EXISTS Atten_Count (
#                 roll text,
#                 course_no text,
#                 number integer
#               )
#               """)


conn.commit()
conn.close()

# def initializedb():
#     conn = sqlite3.connect("Attendance_System.db")
#     cc = conn.cursor()
#     #cc.execute("DROP TABLE Teacher")
#     cc.execute("DROP TABLE Teacher")
#     cc.execute("""
#         CREATE TABLE IF NOT EXISTS Teacher (
#             email text,
#             password text,
#             name text,
#             dept text
#         )""")

#     conn.commit()
#     conn.close()

# def reg():
#     Email = input("Enter Your email Address: ")
#     Pass = input("Enter password: ")
#     Name = input("Enter Name: ")
#     Dept = input("Enter Department: ")

#     conn = sqlite3.connect("Attendance_System.db")

#     cc = conn.cursor()
    
#     data = [(Email,Pass,Name,Dept),
#     ]
#     #data.append(Email)
#     #data.append(Pass)
#     #data.append(Name)
#     #data.append(Dept)
#     cc.executemany("INSERT INTO Teacher VALUES (?,?,?,?)", data)
#     conn.commit()
#     conn.close()

# def show():
#     conn = sqlite3.connect("Attendance_System.db")

#     cc = conn.cursor()

#     cc.execute("SELECT * FROM Teacher")

#     var = cc.fetchall()

#     for item in var:
#         data = item
#         print(data[0]+" "+data[1]+" "+data[2]+" "+data[3])

#     conn.commit()
#     conn.close()







