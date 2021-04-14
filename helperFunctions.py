import qrcode
from openpyxl import load_workbook
import os
import smtplib, ssl
from email.message import EmailMessage
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import datetime

#QR Code Generator
def generateQRCode(msg, filename):
  img = qrcode.make(msg)
  img.save(filename)

#Emailer
def createNewEmailMessage(EMAIL_ADDRESS, listOfContacts, subject, content, xlsxFileName):
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = EMAIL_ADDRESS
  msg['To'] = ', '.join(listOfContacts)
  msg.set_content(content)
  
  with open(xlsxFileName, 'rb') as f:
    file_data = f.read()
    file_name = f.name

  msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename = file_name)
  return msg

def sendEmailWithXlsxAttachment(EMAIL_ADDRESS, PASSWORD, messages):
  context = ssl.create_default_context()
  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(EMAIL_ADDRESS, PASSWORD)
    for msg in messages:
      server.send_message(msg)
  except Exception as e:
    print(e)
  finally:
    server.quit()

def generateExcelSheet(results, name, numOfSeats):
    #Add Extra Empty Records
    valuesWithRecords = {i[3]: None for i in results}
    for desk in range(numOfSeats):
        if desk+1 not in valuesWithRecords:
            results.append(['', '', name, desk+1, ''])

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
    workbook.save(filename=f"{name}_{str(datetime.datetime.now()).split(' ')[0]}.xlsx")
    print('Excel Created')
    return f"{name}_{str(datetime.datetime.now()).split(' ')[0]}.xlsx"