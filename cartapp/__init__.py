# Moving imports and Database creation into an __init__.py file to convert module into package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# All Flask app must create an app instance like this:
app = Flask(__name__)
app.config['SECRET_KEY'] =' sZWjFJmyFQnzkVMxbOIAIZNJhaJV' #setting secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #importing sqldatabase

db = SQLAlchemy(app) #database structure as models

#import routes after app and db initialization to avoid circular importing
from cartapp import routes
