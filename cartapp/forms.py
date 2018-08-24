from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from cartapp.models import User, Order

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])

    password = PasswordField("Password",
                            validators = [DataRequired(), Length(min = 2, max = 20)])

    confirm_password = PasswordField("Confirm Password",
                            validators = [DataRequired(), EqualTo("password")])

    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('This email is already in use')

class ProfileForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    save = SubmitField("Save Changes")

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])

    password = PasswordField("Password", validators = [DataRequired()])

    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class OrderForm(FlaskForm):
    p1 = 549
    p2 = 870
    p3 = 349
    quant_one = IntegerField("", validators = [NumberRange(min = 0, max = 100, message = "min: 0, max: 100")])
    quant_two = IntegerField("", validators = [NumberRange(min = 0, max = 100, message = "min: 0, max: 100")])
    quant_three = IntegerField("", validators = [NumberRange(min = 0, max = 100, message = "min: 0, max: 100")])
    submit = SubmitField("Order now")
