from cartapp import db, login_manager
from flask_login import UserMixin #Additional set up needed to use Login Manager
from datetime import datetime
from cartapp.keys import *
import requests

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    first_name = db.Column(db.String(20), unique = False)
    last_name = db.Column(db.String(20), unique = False)
    token = db.Column(db.String(60))
    refresh_token = db.Column(db.String(60))
    token_expires = db.Column(db.DateTime)

    def update(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        db.session.commit()

    def update_token(self, token, refresh_token, expiry):
        self.token = token
        self.refresh_token = refresh_token
        self.token_expires = expiry
        db.session.commit()

    def delinkCheckbook(self):
        self.token = None
        self.refresh_token = None
        db.session.commit()

    def refresh_token(self):
        #refresh token method here, only called when call to get_token() checks and finds token to be expired
        print("Inside refresh_token() now")
        refresh_headers = {
            'client_id' : client_id,
            'grant_type': 'authorization_code',
            'scope' : ['check'],
            'code': self.token,
            'refresh_token' : self.refresh_token,
            'redirect_uri' : callback_url,
            'client_secret' : api_secret
        }
        response = requests.post(token_url, data = refresh_headers)
        print('post made to token_url with refresh_headers gives:')
        print(response.text)
        #To save new token, simply call update_token passing response data
        

    def get_token(self):
        time_now = datetime.now()
        if time_now > self.token_expires:
            self.refresh_token()
        return self.token

    def __repr__(self):
        return f"User('{ self.email }', {self.id})"

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

    def calcPrice(self):
        self.pricetotal = (self.quant_one*p1) + (self.quant_two*p2) + (self.quant_three*p3)

    def __init__(self):
        self.quant_one = 1;
        self.quant_two = 1;
        self.quant_three = 1;
        self.pricetotal = 0;

    def __repr__(self):
        return f"Order(total:'{ self.pricetotal }', user:'{ self.user_id }', Q1:'{ self.quant_one }', Q2:'{self.quant_two}', Q3:'{self.quant_three}')"
