#####################################################################################################################################

###########  IN ORDER TO GET RID OF ALL THE SPACE CHARACTERS IN A STRING ##############################

# y = '     freed s s sfffeef                 jjujgh   '
# y = y.replace(' ',"")
# print(y)

#####################################################################################################################################


#####  COMMENT START ###########################################################

import sqlite3


# def drop_tables():
#   conn = sqlite3.connect("database.db")
#   c = conn.cursor()
#   c.execute("DROP TABLE STUDENTS")
#   c.execute("DROP TABLE DEPARTMENTS")
#   conn.commit()
#   conn.close()


def createTable():

  conn = sqlite3.connect("database.db")
  c = conn.cursor()

  c.execute("DROP TABLE STUDENTS")
  c.execute("DROP TABLE DEPARTMENTS")

  c.execute("""CREATE TABLE IF NOT EXISTS STUDENTS(
               ROLL TEXT PRIMARY KEY,
               NAME TEXT NOT NULL,
               EMAIL TEXT, 
               DEPARTMENT TEXT ,
               UNIQUE(EMAIL) 
               )""")

  c.execute("""CREATE TABLE IF NOT EXISTS DEPARTMENTS(
               DEPTCODE TEXT PRIMARY KEY,
               DEPTNAME TEXT NOT NULL)""")
  
  conn.commit()
  conn.close()


def insert_into_departments_table():

  conn = sqlite3.connect("database.db")
  c = conn.cursor()

  # c.execute("INSERT INTO STUDENTS VALUES(?,?,?)',('dear','drro','raiyaN')")
  # c.executemany("INSERT INTO DEPARTMENTS VALUES (?)", departments)

  # DELETING ALL ROWS
  c.execute("DELETE FROM DEPARTMENTS" ) 

  # WORKS PHEW :'
  # c.execute("INSERT INTO DEPARTMENTS VALUES (?)", ('CSE',) ) 
  # c.execute("INSERT INTO DEPARTMENTS VALUES (?)", ('EEE',) ) 
  # c.execute("INSERT INTO DEPARTMENTS VALUES (?)", ('ME',) ) 
  # c.execute("INSERT INTO DEPARTMENTS VALUES (?)", ('IT',) ) 

  departments = [ 
                   ('07','CSE'),
                   ('05','EEE'),
                   ('11','ME'),
                ]

  c.executemany("INSERT INTO DEPARTMENTS VALUES (?,?)", departments ) 

  

  # WORKS PHEW :'
  # https://docs.python.org/2/library/sqlite3.html

  # t = ('PE',)
  # c.execute("INSERT INTO DEPARTMENTS VALUES (?)", t ) 

  # DELETING A ROW
  # c.execute("DELETE FROM DEPARTMENTS WHERE NAME=?", ('PE',) ) 




  conn.commit()
  conn.close()

def show_from_departments_table():

  conn = sqlite3.connect("database.db")
  c = conn.cursor()
  

  # row = c.execute("SELECT * FROM DEPARTMENTS").fetchall()
  # print(row)


  # c.fetchone()
  # c.fetchmany(3)
  # results = c.fetchall()
  # print(results)

  for row in c.execute("SELECT * FROM DEPARTMENTS"):
    print(row)

  conn.commit()
  conn.close()

def show_from_students_table():

  conn = sqlite3.connect("database.db")
  c = conn.cursor()

  # row = c.execute("SELECT * FROM DEPARTMENTS").fetchall()
  # print(row)


  # c.fetchone()
  # c.fetchmany(3)
  # results = c.fetchall()
  # print(results)
  
  # conditional query
  # c.execute("SELECT * FROM STUDENTS WHERE DEPARTMENT='CSE'")

  for row in c.execute("SELECT * FROM STUDENTS"):
    print(row)

  conn.commit()
  conn.close()



def insert_into_students_table(roll,name,email,dept):

  conn = sqlite3.connect("database.db")
  c = conn.cursor()

  # students = [('20','pipi','pipi@gmail.com',''),()]

  # c.execute("INSERT INTO STUDENTS VALUES(?,?,?)',('dear','drro','raiyaN')")
  # c.execute("INSERT INTO STUDENTS VALUES(,,,)")


  # c.execute("DELETE FROM STUDENTS" ) 
  c.execute("INSERT INTO STUDENTS VALUES(?,?,?,?)",(roll,name,email,dept))


  conn.commit()
  conn.close()



##############################################################################################################################


createTable()
insert_into_departments_table()
# show_from_departments_table()


insert_into_students_table('25','gigi','gigi@gmail.com','IT')
insert_into_students_table('20','hadid','hadit@gmail.com','CSE')
insert_into_students_table('152','huhu','huhu@gmail.com','CSE')
insert_into_students_table('150','meme','meme@gmail.com','ME')

show_from_students_table()
