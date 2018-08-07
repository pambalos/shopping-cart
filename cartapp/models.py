from cartapp import db

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

    def calcPrice(self):
        self.pricetotal = (self.quant_one*p1) + (self.quant_two*p2) + (self.quant_three*p3)

    def __init__(self):
        self.quant_one = 1;
        self.quant_two = 1;
        self.quant_three = 1;
        self.pricetotal = 0;

    def __repr__(self):
        return f"Order(total:'{ self.pricetotal }', user:'{ self.user_id }', Q1:'{ self.quant_one }', Q2:'{self.quant_two}', Q3:'{self.quant_three}')"
