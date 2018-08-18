from flask import render_template, url_for, flash, redirect, session, request
from cartapp import app, db
from cartapp.forms import OrderForm, RegistrationForm, LoginForm, ProfileForm
from cartapp.models import User, Order
from cartapp import bcrypt, oauth
from flask_login import login_user, current_user, logout_user
from requests_oauthlib import OAuth2Session
from cartapp.keys import *
import requests, json

@app.route('/')
@app.route('/shop', methods = ['GET', 'POST'])
def shop():
    form = OrderForm()
    if form.validate_on_submit():
        return render_template('displayCart.html', title = 'Cart', form = form)
    return render_template('index.html', title = 'Shop', form = form)


@app.route('/home', methods = ['GET', 'POST'])
def home():
    form = OrderForm()
    if form.validate_on_submit():
        flash(f'Order made for {form.quant_one.data} :q1, {form.quant_two.data}: q2, {form.quant_three.data}: q3', 'success')
        print("Order submitted with q1: " + form.quant_one.data + " q2: " + form.quant_two.data + " q3: " + form.quant_three.data)
    return render_template('displayCart.html', title = 'Cart', form = form)

@app.route('/about')
def about():
    
    return render_template('about.html', title = 'About')


@app.route('/dev', methods = ['GET', 'POST'])
def check():
    form = OrderForm()
    if form.validate_on_submit():
        flash(f'Order made for {form.quant_one.data} :q1, {form.quant_two.data}: q2, {form.quant_three.data}: q3', 'success')
        print("Order submitted with q1: " + form.quant_one.data + " q2: " + form.quant_two.data + " q3: " + form.quant_three.data)
        return render_template('home.html', title = 'Home', form = form)
    return render_template('cartForm.html', title = 'Dev', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user) # if does not work try editing to login_user(user, remember = True)
            flash(f'Login Successful', 'success')
            return redirect(url_for('profile'))
        else:
            flash(f'Login failed, please check email and password', 'danger')
    return render_template('login.html', title = "Login", form = form)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = current_user.email).first()
        user.update(form.email.data, form.first_name.data, form.last_name.data)
    return render_template('profile.html', title = 'Profile', form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashp = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(email = form.email.data, password = hashp)
        db.session.add(user)
        db.session.commit()
        flash(f'Account for {form.email.data} created, you may now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/authorize') #Authorization call to direct user to checkbook for login
def authorize():
    cbook = OAuth2Session(client_id, scope = 'check')
    authorization_url, state = cbook.authorization_url(auth_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback', methods = ["GET", "POST"])
def callback():
    cbook = OAuth2Session(client_id, redirect_uri = callback_url, state = session['oauth_state'])
    codebase = str(request.url)
    trash, acode = codebase.split("code=") #acode now holds parsed authorization code passed back in redirect header

    token_headers = {
        'client_id' : client_id,
        'grant_type': 'authorization_code',
        'scope' : 'check',
        'code' : acode,
        'redirect_uri' : 'http://127.0.0.1:5000/callback',
        'client_secret' : api_secret
    }

    response = requests.request("POST", token_url, headers = token_headers)
    print('POST request attempted and completed')
    print(response.text)

    return redirect(url_for('profile'))
