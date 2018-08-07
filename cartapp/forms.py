from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                            validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField("Email", validators = [DataRequired(), Email()])

    password = PasswordField("Password",
                            validators = [DataRequired(), Length(min = 2, max = 20)])

    confirm_password = PasswordField("Confirm Password",
                            validators = [DataRequired(), EqualTo("password")])

    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [])

    username = StringField("Username",
                            validators = [])

    password = PasswordField("Password",
                            validators = [DataRequired()])

    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class OrderForm(FlaskForm):
    quant_one = IntegerField("", validators = [NumberRange(min = 0, max = 100, message = "min: 0, max: 100")])
    quant_two = IntegerField("", validators = [NumberRange(min = 0, max = 100, message = "min: 0, max: 100")])
    quant_three = IntegerField("", validators = [NumberRange(min = 0, max = 100, message = "min: 0, max: 100")])
    submit = SubmitField("Order Now")
