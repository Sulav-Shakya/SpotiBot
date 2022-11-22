import git
import requests
import json
from email.mime import base
from wsgiref import headers
from flask import Flask,redirect, jsonify, session
from flask import request
from urllib.parse import urlencode,urlparse,parse_qs
import string
import random
import base64

#from requests import request
app = Flask(__name__)
app.secret_key = "absjwodwiduwnmdwjdh00e22"
REDIRECT_URI = 'http://sshakya.pythonanywhere.com/callback'
CLIENT_ID = '638c169da9de408c869a924c9a1d2b31'
CLIENT_SECRET = 'f88778a4548d48c8ab5440e0c4bfd4bf'
REFRESH_TOKEN = " "
ACCESS_CODE = " "

#random string for security used later
def randomString(n):
    return ''.join (random.choices(string.ascii_letters+string.digits,k=n))

#base64 encode method, required by Spotify as an input for one of their post requests
def base64Encode(s):
    stringBytes = s.encode("ascii")
    base64Bytes = base64.b64encode(stringBytes)
    base64String = base64Bytes.decode("ascii")
    return base64String







#login endpoint, user is directed to visit this from discord
@app.route("/login")
def login():
    parsedUrl = urlparse(request.url)
    values = parse_qs(parsedUrl.query)

    userID = values.get('userID')[0]

    with open('/home/SSHAKYA/mysite/userTokens.json', 'r') as f:
        data = json.load(f)

    #gets user id from http data to be stored within the app for later use
    session["userID"] = userID


    if(data["users"].get(userID) == None):
        data["users"].update({userID : None})

    with open('/home/SSHAKYA/mysite/userTokens.json', 'w') as f:
        json.dump(data,f, indent=  4)


    authData = {
        "client_id" : CLIENT_ID,
        "response_type" : 'code',
        "redirect_uri" : REDIRECT_URI,
        "state" : randomString(16),
        "scope" :"user-top-read",
        "show_dialog": True
    }


    return redirect('https://accounts.spotify.com/authorize?'+urlencode(authData))

#callback endpoint that is the main motion for the oAuth process
#after the user has verified that they are okay with letting SpotiBot use the selected data they are redirected to this endpoint
#Spotify appends a code to this redirected url to make sure no funny buisness is going on with where the user is being redirected, and they require this code for the final step of oAuth
@app.route("/callback")
def getToken():
    current_user = session.get("userID", None)
    parsedUrl = urlparse(request.url)
    values = parse_qs(parsedUrl.query)

    #finds the code variable spotify adds on
    code = values.get('code')[0]
    state = values.get('state')[0]


    #request parameters for the post request that spotify asks for
    tokenParams = {
        "grant_type" : "authorization_code",
        "code" : code,
        "redirect_uri" : REDIRECT_URI,
        "client_id" : CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "show_dialog": True
    }


    tokenHeaders = {
        "content-type" : 'application/x-www-form-urlencoded'
    }


    r = requests.post('https://accounts.spotify.com/api/token', data = tokenParams, headers = tokenHeaders)

    #catches refresh and access code
    REFRESH_TOKEN = r.json().get("refresh_token")
    ACCESS_CODE =r.json().get("access_token")

    #uses stored discord user id from before to store the value of the user with the associated values
    with open('/home/SSHAKYA/mysite/userTokens.json', 'r') as f:
        data = json.load(f)


    with open('/home/SSHAKYA/mysite/userTokens.json', 'w') as f:


        data["users"].update({current_user : r.json()})


        json.dump(data,f, indent=  4)

    #once the post request has been sucessfully made and the data has been stored, simply returns to discord
    return redirect("https://discord.com/")


#refresh endpoint that is called when the program detects that an authorized user's access token has been timed out and provides a new one
@app.route("/refresh", methods = ["POST", "GET"])
def getRefreshToken():
    parsedUrl = urlparse(request.url)
    values = parse_qs(parsedUrl.query)
    userID = values.get('userID')[0]


    parsedUrl = urlparse(request.url)
    values = parse_qs(parsedUrl.query)


    state = values.get('state')
    with open('/home/SSHAKYA/mysite/userTokens.json', 'r') as f:
        data = json.load(f)
        tokenParams = {
            "grant_type" : "refresh_token",
            "refresh_token" : data.get("users").get(userID).get("refresh_token"),
            "redirect_uri" : REDIRECT_URI,
            "client_id" : CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }

    tokenHeaders = {
        "content-type" : 'application/x-www-form-urlencoded'
    }

    r = requests.post('https://accounts.spotify.com/api/token', data = tokenParams, headers = tokenHeaders)

    return r.json()












