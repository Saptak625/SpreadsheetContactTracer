# Python standard libraries
import json
import os
import sqlite3
import datetime

# Third-party libraries
from flask import Flask, redirect, request, url_for, render_template, abort, session, flash, send_file, send_from_directory, safe_join
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import zipfile
import os

from oauthlib.oauth2 import WebApplicationClient
import requests

from forms import CreateNewClassroomForm, ContactTracingForm, DeskAssociationsForm
from Classroom import Classroom
from ContactTracingAlgorithm import CovidExposure

# Internal imports
from db import init_db_command
from dbFunctions import init_db_local, queryByName, createNewEntry, getClassroomsByUser
from user import User

# Configuration
GOOGLE_CLIENT_ID = '1035349127617-qqodm7fsrlo8akvjds7hkttc3iavf2vd.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'Qi9Iy-b-I96wT7hJn47kTapR'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
application = Flask(__name__)
# app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
application.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(application)

# Naive database setup
# try:
#     init_db_command()
# except sqlite3.OperationalError:
#     # Assume it's already been created
#     pass

# try:
#     init_db_local()
# except sqlite3.OperationalError:
#     # Assume it's already been created
#     pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@application.route("/manageclasses")
def manageClasses():
    if current_user.is_authenticated:
        #Get all classes owned by user.
        classroomResults = getClassroomsByUser(current_user)
        return render_template('manageclasses.html', classroomResults=classroomResults)
    else:
        return redirect(url_for('teacherLogin'))

@application.route("/recordentry")
def recordEntry():
    if current_user.is_authenticated:
        if 'classroomid' not in session and 'seat' not in session:
            abort(404)
        classroomid = session['classroomid']
        seat = session['seat']
        if classroomid == None or seat == None:
            abort(404)
        #Log Entry in Database
        createNewEntry(current_user, classroomid, seat)
        #Flash Confirmation message
        flash(f'{current_user.name} was successfully logged in!', 'success')
        name = current_user.name
        logout_user()
        session.pop('classroomid', None)
        session.pop('seat', None)
        return render_template('confirmation.html', name=name, classroomid=classroomid, seat=seat)
    else:
        classroomid = request.args.get('classroomid')
        seat = request.args.get('seat')
        if classroomid == None or seat == None:
          abort(404)
        #Check if classroom exists in database
        databaseResults = queryByName(classroomid)
        if databaseResults == None:
           abort(404)
        if not seat <= databaseResults[3]:
            abort(404)
        session['classroomid'] = classroomid
        session['seat'] = seat
        return redirect(url_for('studentLogin'))

@application.route('/deskassociations/<path:path>', methods=['GET', 'POST'])
def deskAssociations(path):
    #Do validation on class ownership etc.
    form = DeskAssociationsForm()
    submitted = False
    if form.validate_on_submit():
        submitted = True
    return render_template("deskassociations.html", form=form, submitted = submitted)


@application.route('/Zips/<path:path>', methods=['GET', 'POST'])
def downloadZipFile(path):
    if not current_user.is_authenticated:
        abort(403)
    #Check if classroom exists in database and user owns the class
    results = queryByName(path[:-4])
    if results == None:
        abort(404)
    if results[4] != current_user.email:
        abort(403)
    #Class Exists -> generateQRCodes
    classroom = Classroom(results[0], results[2], results[3], from_database = True)
    classroom.generateQRCodes()
    try:
        return send_file(f'{path}',
            mimetype = 'zip',
            attachment_filename=f'{path}',
            as_attachment = True)
    except FileNotFoundError:
        abort(404)

@application.route('/Excel/<path:path>', methods=['GET', 'POST'])
def downloadExcelFile(path):
    if not current_user.is_authenticated:
        abort(403)
    #Check if classroom exists in database and user owns the class
    results = queryByName(path[:-5])
    if results == None:
        abort(404)
    if results[4] != current_user.email:
        abort(403)
    #Class Exists -> generateExcelReport
    classroom = Classroom(results[0], results[2], results[3], from_database = True)
    filepath = classroom.generateExcelReport()
    try:
        return send_file(filepath, attachment_filename=filepath, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# Manual Reset only
@application.route("/reset")
def reset():
    from reset import resetAndArchive
    resetAndArchive()
    return """<h1>RESET COMPLETE</h1>"""

@application.route("/teacherhomepage")
def teacherHomepage():
    if current_user.is_authenticated:
        return render_template("teacherHomepage.html", current_user=current_user)
    else:
        return redirect(url_for('teacherLogin'))

@application.route("/contacttrace", methods=['GET', 'Post'])
def contactTrace():
    #Do admin validation using dasd contact tracer email.
    form = ContactTracingForm()
    submitted = False
    if form.validate_on_submit():
        email=str(request.form['email'])
        dateList=request.form['startDate'].split('/')
        maxChainLength=int(request.form['maxChainLength'])
        startDate=datetime.datetime(int(dateList[2]), int(dateList[0]), int(dateList[1]), 0, 0, 0, 0)
        CovidExposure.numOfIterations = maxChainLength
        startNode = CovidExposure(email, startDate)
        submitted = True
    return render_template("contacttrace.html", form=form, submitted = submitted)

@application.route("/createclass", methods=['GET', 'Post'])
def createClass():
    if current_user.is_authenticated:
        form = CreateNewClassroomForm()
        classInfo = {}
        submitted = False
        if form.validate_on_submit():
            name=str(request.form['name'])
            numOfSeats=int(request.form['numOfSeats'])
            physicalName = str(request.form['physicalName'])
            classroom = Classroom(name, numOfSeats, current_user, roomId=physicalName)
            flash("Class Created Successfully!", 'success')
            classInfo = {'name': name, 'numOfSeats': numOfSeats, 'qrPath': classroom.generateQRCodes(), 'physicalName': physicalName}
            submitted = True
        return render_template("createClass.html", form=form, classInfo=classInfo, submitted=submitted)
    else:
        return redirect(url_for('teacherLogin'))

@application.route("/teacherprelogin")
def teacherPrelogin():
    logout_user()
    flash('Logout Successful!', 'success')
    return render_template("teacherPrelogin.html")

@application.route("/studentlogin")
def studentLogin():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@application.route("/studentlogin/callback")
def studentCallback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["name"]
    else:
        return "User email not available or not verified by Google.", 

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("recordEntry"))

@application.route("/teacherlogin")
def teacherLogin():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@application.route("/teacherlogin/callback")
def teacherCallback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["name"]

        #MAKE SURE USER IS TEACHER: DASD TEACHER ONLY
        # if '@dasd.org' not in users_email:
        #     abort(403)
    else:
        return "User email not available or not verified by Google.", 

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("teacherHomepage"))


if __name__ == "__main__":
    #Development only
    application.run(debug=True, ssl_context="adhoc")