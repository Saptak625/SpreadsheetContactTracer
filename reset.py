from Classroom import Classroom
from user import User
from helperFunctions import sendEmailWithXlsxAttachment
import datetime
import os
from dbFunctions import fetchAllClassrooms
import sqlite3

def resetAndArchive():
    #SEND ALL EMAILS
    classroomList = fetchAllClassrooms()
    classrooms = [Classroom(props[0], props[1], User(None, props[2], props[3], None), from_database=True) for props in classroomList]
    EMAIL_ADDRESS = 'dasdcontacttracer.noreply@gmail.com'
    PASSWORD = 'iaqbetokntxxhxvi'
    for classroom in classrooms:
        filename = classroom.generateExcelReport()
        #SEND EMAILS TO EVERY TEACHER
        contacts = [classroom.owner.email]
        msg_subject = f"Report for Class {classroom.name} on {str(datetime.datetime.now()).split(' ')[0]}"
        msg_content = f"Attached is the report for Class {classroom.name} on {str(datetime.datetime.now()).split(' ')[0]}."
        sendEmailWithXlsxAttachment(EMAIL_ADDRESS, PASSWORD, contacts, msg_subject, msg_content, filename)
    #CLEAR ALL ENTRIES
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE entries")
    connection.commit()
    connection.close()
    #INIT ENTRIES TABLE
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE entries (name TEXT, email TEXT, classroomid TEXT, deskNumber INTEGER, entryTime TEXT)")
    connection.commit()
    connection.close()
    #EMPTY EXCEL AND ZIPS FOLDERS
    test = os.listdir()
    print(test)
    for item in test:
        if item.endswith(".zip") or item.endswith(".xlsx"):
            os.remove(item)
    # filelist = [ f for f in os.listdir('Excel') ]
    # for f in filelist:
    #     os.remove(os.path.join('Excel', f))
    # filelist = [ f for f in os.listdir('Zips') ]
    # for f in filelist:
    #     os.remove(os.path.join('Zips', f))