# SpreadsheetContactTracer

## How it Works?
### Teachers/Admin
Teachers/Admin play the following roles in this application:
* Creator and Manager of Classrooms
* Access Classroom Information such as QR Codes and Excel Reports
* Recipient of Daily Email for Contact Tracing Records in form of Excel file

### Students
Students play the following roles in this application:
* Scan QR Codes to log information accordingly. The more strictly followed, the better the contact tracing results will be.

## Most Recent Stable Release: Release 2.0
This release has:

### Integrated Features:
* 2 distinct Google Login links for teachers and students
* Flask Webage Flow
* Protection from common cyberattacks(SQL Injection, CSRF, etc.) 
* Flask-Login + User Model + User Database
* Jinja2 + Flask: Html render_template
* Integration of QR Generation, Packaging data into Excel files, and Emailing of these Excel Files
* Executable Batch File(reset.bat) to be triggered using Cron Job(local or server)
* Auto-Generated Physical Classroom Concept for Admin Contatc Tracing

### Other Nice-to-have Features to be released in Future Releases:
* Classroom Resizing(Enable classrooms to get smaller or larger if teachers are assigned a new room)
* Automation of Contact Tracing through another local-based program. This would include features to associate desks(treating multiple virtual locations as one physical location). This could extract data from the email archives and perform needed searches to allow for a more methodical way to contact trace.
