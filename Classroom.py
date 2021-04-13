from dbFunctions import addClassroom, queryByName, queryForEntries
import sys
import os
from helperFunctions import generateQRCode
from zipfile import ZipFile
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import datetime

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
        
        #Add Extra Empty Records
        valuesWithRecords = {i[3]: None for i in results}
        for desk in range(self.numOfSeats):
            if desk+1 not in valuesWithRecords:
                results.append(['', '', self.name, desk+1, ''])

        #Sort Results by desks
        def sortByDeskNumber(e):
          return e[3]
        results.sort(key=sortByDeskNumber)  

        #Create New Excel File
        workbook = Workbook()
        sheet = workbook.active

        #Make Header
        headerTitles = ['Desk', 'Name', 'Email', 'Time']
        ordOfA = ord('A')
        for i, header in enumerate(headerTitles):
          sheet[f'{chr(ordOfA+i)}1'] = header
          sheet[f'{ chr(ordOfA+i) }1'].font = Font(bold=True)

        #Make entries one by one
        deskNumbers = {}
        lastNumber = None
        for i, entry in enumerate(results):
            sheet[f'A{i+2}'] = entry[3]
            sheet[f'A{i+2}'].alignment = Alignment(horizontal='center', vertical='center')
            sheet[f'B{i+2}'] = entry[0]
            sheet[f'C{i+2}'] = entry[1]
            sheet[f'D{i+2}'] = entry[4]
            if lastNumber != entry[3]:
                if lastNumber != None:
                    deskNumbers[lastNumber].append(i+2-1)
                lastNumber = entry[3]
                deskNumbers[lastNumber] = [i+2]
        if lastNumber != None:
            deskNumbers[lastNumber].append(len(results)-1+2)
        #Merge Desk Number
        for key in deskNumbers:
          value = deskNumbers[key]
          if value[0] != value[1]:
            #Merge cells
            sheet.merge_cells(f'A{value[0]}:A{value[1]}')
            sheet[f'A{value[0]}']

        #Save File once edits are made
        workbook.save(filename=f"{self.name}_{str(datetime.datetime.now()).split(' ')[0]}.xlsx")
        return f"{self.name}_{str(datetime.datetime.now()).split(' ')[0]}.xlsx"
