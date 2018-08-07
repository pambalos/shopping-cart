from shop import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{ self.email }', '{ self.id }', '{ self.password }')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quant_one = db.Column(db.Integer, default = '0')
    quant_two = db.Column(db.Integer, default = '0')
    quant_three = db.Column(db.Integer, default = '0')
    pricetotal = db.Column(db.Integer, default = '0')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self):
        quant_one = 0;
        quant_two = 0;
        quant_three = 0;
        pricetotal = 0;

    def __repr__(self):
        return f"Order(total:'{ self.pricetotal }', user:'{ self.user_id }', Q1:'{ self.quant_one }', Q2:'{self.quant_two}', '{self.quant_three}')"
