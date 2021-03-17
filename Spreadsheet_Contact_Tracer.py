from flask import Flask, render_template, request, redirect, url_for, abort
from Functions import generateQRCode, editSpreadsheet
from oauthlib.oauth2 import WebApplicationClient
from User import User
import requests
import json
import os
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

GOOGLE_CLIENT_ID = '1035349127617-qqodm7fsrlo8akvjds7hkttc3iavf2vd.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'Qi9Iy-b-I96wT7hJn47kTapR'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

queryParameters = []

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route('/createclassroom')
def createClassroomPage():
    return render_template('createClassroom.html')

# @app.route('/adduser')
# def addUserPage():
#     user = request.args.get('classroomid')
#     print(user, type(user))
#     return render_template('addUser.html')

@app.route("/login")
def login():
    classroomid = request.args.get('classroomid')
    seat = request.args.get('seat')
    queryParameters.append(classroomid)
    queryParameters.append(seat)
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
    print()
    print(request_uri)
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
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
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 

    # Create a user in your db with the information provided
    # by Google
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )

    # # Doesn't exist? Add it to the database.
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)

    user = User(unique_id, users_name, users_email)
    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("confirmation"))

@app.route("/confirmation")
def confirmation():
    #Confirmation
    if len(queryParameters) == 0:
        abort(404)
    return render_template("confirmation.html")



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, ssl_context="adhoc")