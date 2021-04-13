from Classroom import Classroom
from user import User
from helperFunctions import sendEmailWithXlsxAttachment, generateExcelSheet, createNewEmailMessage
import datetime
import os
from dbFunctions import fetchAllClassrooms, queryByPhysicalEntries
import sqlite3

def resetAndArchive():
    #SEND ALL EMAILS
    classroomList = fetchAllClassrooms()
    classrooms = [Classroom(props[0], props[2], User(None, props[3], props[4], None), from_database=True) for props in classroomList]
    EMAIL_ADDRESS = 'dasdcontacttracer.noreply@gmail.com'
    PASSWORD = 'iaqbetokntxxhxvi'
    print('Classrooms', classrooms)
    msgList = []
    for classroom in classrooms:
        print('Class', classroom.name)
        filename = classroom.generateExcelReport()
        #SEND EMAILS TO EVERY TEACHER
        contacts = [classroom.owner.email]
        msg_subject = f"Report for Class {classroom.name} on {str(datetime.datetime.now()).split(' ')[0]}"
        print('Email Prep Complete')
        msg_content = f"Attached is the report for Class {classroom.name} on {str(datetime.datetime.now()).split(' ')[0]}."
        msgList.append(createNewEmailMessage(EMAIL_ADDRESS, contacts, msg_subject, msg_content, filename))
    #sendEmailWithXlsxAttachment(EMAIL_ADDRESS, PASSWORD, msgList)
    print('Sending Email')
    print('Finished generating emails')
    #SEND ALL ADMIN EMAILS
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    physicalClassrooms = cursor.execute("SELECT name, numOfSeats FROM physicalclassroom").fetchall()
    connection.commit()
    connection.close()
    msgList = []
    for pc in physicalClassrooms:
        results = queryByPhysicalEntries(pc[0])
        print('Results', results)
        filename = generateExcelSheet(results, pc[0], pc[1])
        #SEND EMAILS TO EVERY TEACHER
        contacts = [EMAIL_ADDRESS]
        msg_subject = f"Report for Room {pc[0]} on {str(datetime.datetime.now()).split(' ')[0]}"
        msg_content = f"Attached is the report for Room {pc[0]} on {str(datetime.datetime.now()).split(' ')[0]}."
        msgList.append(createNewEmailMessage(EMAIL_ADDRESS, contacts, msg_subject, msg_content, filename))
    #sendEmailWithXlsxAttachment(EMAIL_ADDRESS, PASSWORD, msgList)
    #CLEAR ALL ENTRIES
    print('Deleting Table')
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
    print('Starting file removal')
    test = os.listdir()
    print(test)
    for item in test:
        if item.endswith(".zip") or item.endswith(".xlsx"):
            os.remove(item)
    print('FINISHED')