from flask import render_template, url_for, flash, redirect, session, request
from cartapp import app, db
from cartapp.forms import OrderForm, RegistrationForm, LoginForm, ProfileForm
from cartapp.models import User, Order
from cartapp import bcrypt, oauth
from flask_login import login_user, current_user, logout_user, login_required
from requests_oauthlib import OAuth2Session
from cartapp.keys import *
import requests, json, time
from datetime import datetime, timedelta

@app.route('/shop', methods = ['GET', 'POST'])
@login_required
def shop():
    form = OrderForm()
    print('Created a form at least')
    if form.validate_on_submit():
        print(form)
        displayCart(form)
        order = {}
        order['quant_one'] = form.quant_one.data
        order['quant_two'] = form.quant_two.data
        order['quant_three'] = form.quant_three.data

        return render_template('displayCart.html', title = 'Cart', form = form)
    return render_template('index.html', title = 'Shop', form = form)

@app.route('/displayCart', methods = ['GET', 'POST'])
def displayCart(form):
    form = form
    if form.validate_on_submit():
        flash(f'Submit final order processed', 'success')
    return render_template('displayCart.html', title = 'Cart', form = form)

@app.route('/', methods = ['GET', 'POST'])
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
            login_user(user, remember = form.remember.data) # if does not work try editing to login_user(user, remember = True)
            next_page = request.args.get('next') #request.args is a dictionary but accessing with ['next'] would throw an error if nonexistent
            flash(f'Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash(f'Login failed, please check email and password', 'danger')
    return render_template('login.html', title = "Login", form = form)

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if 'save' in request.form:
            user = User.query.filter_by(email = form.email.data).first()
            if form.email.data != current_user.email and user is not None:
                flash(f'The email address "{form.email.data}" is already in use.', 'danger')
            else:
                user.update(form.email.data, form.first_name.data, form.last_name.data)
        if 'delink' in request.form:
            user = User.query.filter_by(email = current_user.email).first()
            #user.delinkCheckbook()
            user.refresh_token()
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
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/authorize') #Autho rization call to direct user to checkbook for login
def authorize():
    cbook = OAuth2Session(client_id, scope = 'check')
    authorization_url, state = cbook.authorization_url(auth_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback', methods = ["GET", "POST"])
def callback():
    # cbook = OAuth2Session(client_id, redirect_uri = callback_url, state = session['oauth_state'])
    codebase = str(request.url)
    trash, acode = codebase.split("code=") #acode now holds parsed authorization code passed back in redirect header

    token_headers = {
        'client_id' : client_id,
        'grant_type': 'authorization_code',
        'scope' : ['check'],
        'code' : acode,
        'redirect_uri' : callback_url,
        'client_secret' : api_secret
    }

    response = requests.post(token_url, data = token_headers) #proper request formatting
    time_requested = datetime.now()
    response_data = json.loads(response.text) #load data in as dictionary
    time_expires = time_requested + timedelta(seconds = response_data['expires_in'])
    print('time requested : %s' % time_requested)
    print('time expires : %s' % time_expires)
    print(response.text)
    print(response_data["access_token"])
    print(response_data["refresh_token"])
    print(response_data["expires_in"])
    user = User.query.filter_by(email = current_user.email).first()
    user.update_token(response_data["access_token"], response_data["refresh_token"], time_expires)
    flash(f'You have successully linked your checkbook account.', 'success')
    return redirect(url_for('profile'))
