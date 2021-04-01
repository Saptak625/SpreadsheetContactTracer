import qrcode
from openpyxl import load_workbook
import os
import smtplib, ssl
from email.message import EmailMessage


#QR Code Generator
def generateQRCode(msg, filename):
  img = qrcode.make(msg)
  img.save(filename)

#Emailer
def sendEmailWithXlsxAttachment(EMAIL_ADDRESS, PASSWORD, listOfContacts, subject, content, xlsxFileName):
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = EMAIL_ADDRESS
  msg['To'] = ', '.join(listOfContacts)
  msg.set_content(content)

  with open(xlsxFileName, 'rb') as f:
    file_data = f.read()
    file_name = f.name

  msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename = file_name.split('/')[1])

  context = ssl.create_default_context()
  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(EMAIL_ADDRESS, PASSWORD)
    server.send_message(msg)
  except Exception as e:
    print(e)
  finally:
    server.quit()