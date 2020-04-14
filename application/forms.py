from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
    user_name = StringField("User Name", validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField("Register Now")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use, pick another one.")

class FlagNews(FlaskForm):
    url =  StringField("Url", validators=[DataRequired(), Length(min=5, max=5000)])
    topic =  StringField("Topic", validators=[DataRequired()])
    submission_time = DateTimeField("Submission Time")
    submit = SubmitField("Flag Url")

    # count = StringField()

