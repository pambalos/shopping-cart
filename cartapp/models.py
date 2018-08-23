from cartapp import db, login_manager
from flask_login import UserMixin #Additional set up needed to use Login Manager

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
    rToken = db.Column(db.String(60))

    def update(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        db.session.commit()

    def update_token(self, token, rToken):
        self.token = token
        self.rToken = rToken
        db.session.commit()

    def __repr__(self):
        return f"User('{ self.email }', {self.id})"

class Order(db.Model, UserMixin):
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
