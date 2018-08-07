
import requests, json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_oauthlib.client import OAuth
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
app.config['SECRET_KEY'] ='sZWjFJmyFQnzkVMxbFCTbByZNJhaJV' #setting secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{ self.email }', '{ self.id }', '{ self.password }')"

class Order(db.Model):
    p1 = 549
    p2 = 870
    p3 = 349
    id = db.Column(db.Integer, primary_key = True)
    quant_one = db.Column(db.Integer, default = '0')
    quant_two = db.Column(db.Integer, default = '0')
    quant_three = db.Column(db.Integer, default = '0')
    pricetotal = db.Column(db.Integer, default = '0')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self):
        self.quant_one = 1;
        self.quant_two = 1;
        self.quant_three = 1;
        self.pricetotal = 0;

    def __repr__(self):
        return f"Order(total:'{ self.pricetotal }', user:'{ self.user_id }', Q1:'{ self.quant_one }', Q2:'{self.quant_two}', Q3:'{self.quant_three}')"

testCart = Order()
print(testCart)

@app.route('/')
@app.route('/shop')
def shop():
    cart = Order()
    return render_template('index.html', title = 'Shop', cart = cart)

if __name__ == '__main__':
    app.run(debug=True)
