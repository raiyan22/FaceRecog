import sqlite3
#  THIS WORKSSSSSSSSSSSSSSSSSSSSSSSS
def reg():

    conn = sqlite3.connect("Attendance_System.db")
    cc = conn.cursor()
    # cc.execute("DROP TABLE Course_Alloc")
    cc.execute("""
    CREATE TABLE IF NOT EXISTS Course_Alloc (
        email text ,
        course_no text,
        dept text
    )
    """)

    

    cc.execute("SELECT dept FROM Course")
    bbx1 = cc.fetchall()
    box1=[]
    for i in bbx1:
        if i not in box1:
            print(i[0])
            box1.append(i)
    
    
    # print("dept gula je box1 er moddhe ashche ekhon check kore dekhaitesi: ")
    # for item in box1:
    #     print(item)   

    Dept = box1[1][0]
    data22 = []
    data22.append(Dept)

    cc.execute("SELECT email FROM Teacher WHERE dept=?", data22)
    bbx2 = cc.fetchall()
    box2=[]
    for i in bbx2:
        if i not in box2:
            box2.append(i)

    # print("teacher gula je box2 er moddhe ashche ekhon check kore dekhaitesi: ")
    # for item in box2:
    #     print(item) 

    Email = box2[0][0]
    cc.execute("SELECT course_no FROM Course WHERE dept=?", data22)
    bbx3 = cc.fetchall()
    box3=[]
    for i in bbx3:
        if i not in box3:
            box3.append(i)

    # print("course gula je box3 er moddhe ashche ekhon check kore dekhaitesi: ")
    # for item in box3:
    #     print(item)

    Course_no = box3[1][0]
    data = [(Email,Course_no,Dept),
    ]
    
    # cc.executemany("INSERT INTO Course_Alloc VALUES (?,?,?)", data)
    conn.commit()
    conn.close()

def show():
    conn = sqlite3.connect("Attendance_System.db")
    cc = conn.cursor()
    cc.execute("SELECT * FROM Course_Alloc")
    var = cc.fetchall()
    for item in var:
        data = item
        print(data[0]+" "+data[1]+" "+data[2])

    conn.commit()
    conn.close()

reg()
show() 