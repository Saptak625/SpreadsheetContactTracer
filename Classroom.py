from dbFunctions import addClassroom, queryByName, queryForEntries
import sys
import os
from helperFunctions import generateQRCode, generateExcelSheet
from zipfile import ZipFile

class Classroom:
    def __init__(self, name, numOfSeats, owner, roomId=None, from_database = False):
        self.name = name
        self.roomId = roomId
        self.numOfSeats = numOfSeats
        self.owner = owner
        if not from_database:
            self.addToDatabase()

    def addToDatabase(self):
        addClassroom(self)
        
    def generateQRCodes(self):
        ROOT_PATH = "https://127.0.0.1:5000/"
        newpath = f'{self.name}' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        for i in range(self.numOfSeats):
            generateQRCode(f"{ROOT_PATH}recordentry?classroomid={self.name}&seat={i+1}", f"{self.name}/{self.name}_{i+1}.png")


        # path to folder which needs to be zipped
        directory = f'{self.name}'

        # calling function to get all file paths in the directory
        file_paths = []

        # crawling through directory and subdirectories
        for root, directories, files in os.walk(directory):
            for filename in files:
                # join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        # writing files to a zipfile
        with ZipFile(f'{self.name}.zip','w') as zip:
            # writing each file one by one
            for file in file_paths:
                zip.write(file)
            zip.close()

        #Delete all original files
        for i in range(self.numOfSeats):
            os.remove(f"{self.name}/{self.name}_{i+1}.png")
        os.rmdir(f"{self.name}")
        return self.name + '.zip'

    def generateExcelReport(self): 
        #Get entries for Classroom
        #DO DATABASE SEARCH TO GET ALL CLASSROOMS HERE.
        results = queryForEntries(self.name)
        filename = generateExcelSheet(results, self.name, self.numOfSeats)
        return filename
