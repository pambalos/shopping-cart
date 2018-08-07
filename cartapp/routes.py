from flask import render_template, url_for, flash, redirect, session, request
from cartapp import app
from cartapp.forms import OrderForm, RegistrationForm, LoginForm
from cartapp.models import User, Order

@app.route('/')
@app.route('/shop')
def shop():
    cart = Order()
    return render_template('index.html', title = 'Shop', cart = cart)

@app.route('/dev')
def check():
    form = OrderForm()
    cart = Order()
    return render_template('cartForm.html', title = 'Dev', cart = cart, form = form)
