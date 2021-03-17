import sqlite3

#Creating and Initialing Table(Only execute once)
# connection = sqlite3.connect("classrooms.db")
# cursor = connection.cursor()
# cursor.execute("CREATE TABLE classrooms (name TEXT, timeStart TEXT, timeEnd INTEGER)")

def addClassroom(classroom):
    connection = sqlite3.connect("classrooms.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO classrooms VALUES (?, ?, ?)", [classroom.name, classroom.timeStart, classroom.timeEnd])
    connection.commit()
    connection.close()

def queryByName(queryName):
    connection = sqlite3.connect("classrooms.db")
    cursor = connection.cursor()
    results = cursor.execute(
    "SELECT name, timeStart, timeEnd FROM classrooms WHERE name = ?",
    (queryName,),).fetchall()
    connection.commit()
    connection.close()
    return results

def fetchAllEntries():
    connection = sqlite3.connect("classrooms.db")
    cursor = connection.cursor()
    rows = cursor.execute("SELECT name, timeStart, timeEnd FROM classrooms").fetchall()
    connection.commit()
    connection.close()
    return rows
 