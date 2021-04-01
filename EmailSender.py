import smtplib, ssl
from email.message import EmailMessage
import getpass

EMAIL_ADDRESS = '24sdas@student.dasd.org'
PASSWORD = getpass.getpass()
contacts = [EMAIL_ADDRESS, 'saptak.das625@gmail.com']
msg_subject = 'Test Message with xlsx'
msg_content = 'Test Message Body with xlsx'
filename = 'RightTriangleSolverTestCases.xlsx'

def sendEmailWithXlsxAttachment(EMAIL_ADDRESS, PASSWORD, listOfContacts, subject, content, xlsxFileName):
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = EMAIL_ADDRESS
  msg['To'] = ', '.join(listOfContacts)
  msg.set_content(content)

  with open(xlsxFileName, 'rb') as f:
    file_data = f.read()
    file_name = f.name

  msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename = file_name)

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

sendEmailWithXlsxAttachment(EMAIL_ADDRESS, PASSWORD, contacts, msg_subject, msg_content, filename)