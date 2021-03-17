from dbFunctions import addClassroom, queryByName, fetchAllEntries
import sys

class Classroom:
    def __init__(self, name, timeStart=None, timeEnd=None):
        if(timeStart != None and timeEnd != None):
            self.name = name
            self.timeStart = timeStart
            self.timeEnd = timeEnd
            self.addToDatabase()
        elif(timeStart == None and timeEnd == None):
            queryResults = queryByName(name)
            print(queryResults)

            #CHANGE LOGIC BELOW
            chosenQuery = queryResults[0]
        else:
            print("Not enough or too many fields were passed into initializer to create Classroom.")
            sys.exit(0)

    def addToDatabase(self):
        addClassroom(self)
