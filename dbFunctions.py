import sqlite3
import datetime

def init_db_local():
    #Creating and Initialing Table(Only execute once)
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE classroom (name TEXT, physicalclassroom TEXT, numOfSeats INTEGER, owner TEXT, ownerEmail TEXT)")
    cursor.execute("CREATE TABLE deskAssociations (deskId1 TEXT, deskId2 TEXT)")
    cursor.execute("CREATE TABLE entries (name TEXT, email TEXT, classroomid TEXT, deskNumber INTEGER, entryTime TEXT)")
    cursor.execute("CREATE TABLE physicalclassroom (name TEXT, numOfSeats INTEGER)")
    cursor.execute("CREATE TABLE contacttraceentries (name TEXT, email TEXT, physicalclassroom TEXT, deskNumber INTEGER, entryTime TIMESTAMP)")
    connection.commit()
    connection.close()

def addClassroom(classroom):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO classroom VALUES (?, ?, ?, ?, ?)", [classroom.name, classroom.roomId, classroom.numOfSeats, classroom.owner.name, classroom.owner.email])
    #Default all desk associations
    for desk1 in range(classroom.numOfSeats):
        for desk2 in range(classroom.numOfSeats):
            if desk1 != desk2:
                cursor.execute("INSERT INTO deskAssociations VALUES (?, ?)", [f'{classroom.roomId}_{desk1+1}', f'{classroom.roomId}_{desk2+1}'])
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

def queryByName(queryName):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, physicalclassroom, numOfSeats, owner, ownerEmail FROM classroom WHERE name = ?",
    (queryName,),).fetchone()
    connection.commit()
    connection.close()
    return results

def getClassroomsByUser(user):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, physicalclassroom, numOfSeats, owner, ownerEmail FROM classroom WHERE ownerEmail = ?",
    (user.email,),).fetchall()
    connection.commit()
    connection.close()
    return results

def fetchAllClassrooms():
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    rows = cursor.execute("SELECT name, physicalclassroom, numOfSeats, owner, ownerEmail FROM classroom").fetchall()
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

def checkPhysicalClassroom(physicalClassroom):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, numOfSeats FROM physicalclassroom WHERE name = ?",
    (physicalClassroom,),).fetchone()
    connection.commit()
    connection.close()
    return results

def queryByPhysicalEntries(physicalClassroom):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, physicalclassroom, numOfSeats, owner, ownerEmail FROM classroom WHERE physicalclassroom = ?",
    (physicalClassroom,),).fetchall()
    connection.commit()
    connection.close()
    newEntries = []
    for classroom in results:
        newEntries += queryForEntries(classroom[0])
    return newEntries

def addNewContactTraceEntry(listOfData):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO contacttraceentries VALUES (?, ?, ?, ?, ?)", [listOfData[0], listOfData[1], listOfData[2], int(listOfData[3]), listOfData[4]])
    connection.commit()
    connection.close()

def queryContactTraceEntry(userEmail, upToDate):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, email, physicalclassroom, deskNumber, entryTime FROM contacttraceentries WHERE email = ? AND entryTime <= ?",
    (userEmail, upToDate),).fetchall()
    connection.commit()
    connection.close()
    return results

def findAdjacentDesks(deskId):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT deskId1, deskId2 FROM deskAssociations WHERE deskId1 = ?",
    (deskId),).fetchall()
    connection.commit()
    connection.close()
    #Add current desk as well.
    results.append([deskId, deskId])  
    return results

def getContactedEntries(physicalclassroom, deskNumber, startTime, endTime):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, email, physicalclassroom, deskNumber, entryTime FROM contacttraceentries WHERE physicalclassroom = ? AND deskNumber = ? AND entryTime >= ? AND entryTime <= ?",
    (physicalclassroom, deskNumber, startTime, endTime),).fetchall()
    connection.commit()
    connection.close()
    return results

def checkEmailInDatabase(email):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT id, name, email, profile_pic FROM user WHERE email = ?",
    (email,),).fetchone()
    connection.commit()
    connection.close()
    return results

def checkDeskOwnership(classroomName):
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, physicalclassroom, numOfSeats, owner, ownerEmail FROM classroom WHERE name = ?",
    (classroomName,),).fetchone()
    connection.commit()
    connection.close()
    return results

def getDeskAssociations(classinfo):
    #Get deskIDs
    deskIDs = [f'{classinfo[1]}_{i+1}' for i in range(classinfo[2])]
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    results = []
    for deskId in deskIDs:
        rawData = cursor.execute(
        "SELECT deskId1, deskId2 FROM deskAssociations WHERE deskId1 = ? AND deskId2 != ?",
        (deskId, deskId),).fetchall()
        defaultResults = [False for i in range(classinfo[2])]
        for associations in rawData:
            defaultResults[int(associations[1].split('_')[1])-1] = True
        defaultResults.pop(int(deskId.split('_')[1])-1)
        results.append(defaultResults) 
    connection.commit()
    connection.close()
    return results

def updateDeskAssociations(deskResults, classinfo):
    #Delete all previous associations, except for same pair
    connection = sqlite3.connect("sqlite.db")
    cursor = connection.cursor()
    deskIDs = [f'{classinfo[1]}_{i+1}' for i in range(classinfo[2])]
    for deskId in deskIDs:
        cursor.execute(
            "DELETE FROM deskAssociations WHERE deskId1 = ?",
            (deskId,),)
    for desk1, results in enumerate(deskResults):
        for desk2, boolean in enumerate(results):
            if boolean == True:
                cursor.execute("INSERT INTO deskAssociations VALUES (?, ?)", (deskIDs[desk1], deskIDs[desk2]),)
    connection.commit()
    connection.close()