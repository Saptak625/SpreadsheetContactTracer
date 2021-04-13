import sqlite3
import datetime

def init_db_local():
    #Creating and Initialing Table(Only execute once)
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE classroom (name TEXT, numOfSeats INTEGER, owner TEXT, ownerEmail TEXT)")
    cursor.execute("CREATE TABLE entries (name TEXT, email TEXT, classroomid TEXT, deskNumber INTEGER, entryTime TEXT)")
    cursor.execute("CREATE TABLE physicalclassroom (name TEXT, numOfSeats INTEGER)")
    connection.commit()
    connection.close()

def addClassroom(classroom):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO classroom VALUES (?, ?, ?, ?)", [classroom.name, classroom.numOfSeats, classroom.owner.name, classroom.owner.email])
    connection.commit()
    connection.close()
    #Check if physical classroom exists
    if classroom.roomId != None:
        connection = sqlite3.connect("sqlite.db")
        cursor = connection.cursor()
        results = cursor.execute("SELECT name, numOfSeats FROM physicalclassroom").fetchone()
        if results == None:
            cursor.execute("INSERT INTO physicalclassroom VALUES (?, ?)", [classroom.roomId, classroom.numOfSeats])
        connection.commit()
        connection.close()
        return results


def queryByName(queryName):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, numOfSeats, owner, ownerEmail FROM classroom WHERE name = ?",
    (queryName,),).fetchone()
    connection.commit()
    connection.close()
    return results

def getClassroomsByUser(user):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, numOfSeats, owner, ownerEmail FROM classroom WHERE ownerEmail = ?",
    (user.email,),).fetchall()
    connection.commit()
    connection.close()
    return results

def fetchAllClassrooms():
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    rows = cursor.execute("SELECT name, numOfSeats, owner, ownerEmail FROM classroom").fetchall()
    connection.commit()
    connection.close()
    return rows
 
def createNewEntry(user, classroomid, deskNumber):
    dateString = ':'.join(str(datetime.datetime.now()).split(' ')[1].split(':')[:2])
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO entries VALUES (?, ?, ?, ?, ?)", [user.name, user.email, classroomid, deskNumber, dateString])
    connection.commit()
    connection.close()
    
def queryForEntries(classroomid):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, email, classroomid, deskNumber, entryTime FROM entries WHERE classroomid = ?",
    (classroomid,),).fetchall()
    connection.commit()
    connection.close()
    return results