# Moving imports and Database creation into an __init__.py file to convert module into package
from flask import Flask, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from cartapp.keys import *
# All Flask app must create an app instance like this:
app = Flask(__name__)
app.config['SECRET_KEY'] =' sZWjFJmyFQnzkVMxbOIAIZNJhaJV' #setting secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #importing sqldatabase
db = SQLAlchemy(app) #database structure as models
db.app = app
oauth = OAuth(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#OAuth2 setup
checkbook = oauth.remote_app('checkbook',
    base_url = "https://sandbox.checkbook.io/v3/"
    request_token_url = "https://checkbook.io/oauth/token"
    
    authorize_url = "https://checkbook.io/oauth/authorize"
    consumer_key = api_key
    consumer_secret = api_secret
)

#import routes after app and db initialization to avoid circular importing
from cartapp import routes
