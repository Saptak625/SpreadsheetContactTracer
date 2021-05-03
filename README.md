# SpreadsheetContactTracer

## How it Works?
### Teachers
Teachers play the following roles in this application:
* Creator and Manager of Classrooms
* Access Virtual Classroom Information such as QR Codes and Excel Reports
* Recipient of Daily Email for Contact Tracing Records in form of Excel file
* Editing of Physical Classroom Desk Associations for better Contact Tracing Results(accessed by all teachers of a specific physical classroom)

### Admins
Admins play the following roles in this application:
* Access Physical Classroom Information of Daily Desk Usage Records
* Contact Tracing Algorithm using above information

### Students
Students play the following roles in this application:
* Scan QR Codes to log information accordingly. The more strictly followed, the better the contact tracing results will be.

## Most Recent Stable Release: Release 3.0
This release has:

### Integrated Features:
* 2 distinct Google Login links for teachers and students(Plus validation for admin contact tracing) for ease of use
* Flask Webpage Flow
* Admin Contact Tracing Algorithm that extracts tracing data from up to 14 days ago
* Custom Desk Associations to provide more accurate and targeted Contact Tracing Results(Default is more broad and inclusive and provides more careful results)
* Protection from common cyberattacks(SQL Injection, CSRF, etc.) 
* Flask-Login + User Model + User Database
* Jinja2 + Flask: Html render_template
* Integration of QR Generation, Packaging data into Excel files, Emailing of these Excel Files, and Extraction of Tracing Data from Email for Contact Tracing
* Executable Batch File(reset.bat) to be triggered daily to empty local SQLITE records into Email Dump using Cron Job(local or server)
* Auto-Generated Physical Classroom Structure for Admin Contact Tracing

### Other Nice-to-have Features to be released in Future Releases:
* Classroom Resizing(Enable classrooms to get smaller or larger if teachers are assigned a new room)
* Production Server Deployment(AWS, APACHE, NGINX, etc.)
* Improvements to Contact Tracing Algorithm(Comprehensive Testing + Specific Controls for targeted results)
* UI Beautification(Specific pages could be beautified)
