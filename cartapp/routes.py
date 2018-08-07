from flask import render_template, url_for, flash, redirect, session, request
from cartapp import app
from cartapp.forms import OrderForm, RegistrationForm, LoginForm
from cartapp.models import User, Order

@app.route('/')
@app.route('/shop')
def shop():
    cart = Order()
    return render_template('index.html', title = 'Shop', cart = cart)


@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/dev')
def check():
    form = OrderForm()
    cart = Order()
    return render_template('cartForm.html', title = 'Dev', cart = cart, form = form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = "Login", form = form)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title = 'Register', form = form)
