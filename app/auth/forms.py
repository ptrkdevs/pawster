from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired("name cannot be empty.")])
    email = StringField(
        "Email",
        validators=[
            DataRequired("Email cannot be empty."),
            Email("Should be a valid email"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired("password cannot be empty")]
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired("password cannot be empty"), EqualTo("password")],
    )

    submit = SubmitField("Sign up")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("username already taken.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():

            raise ValidationError("email already has an account.")


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password")

    submit = SubmitField("Sign in")


class UpdateForm(FlaskForm):

    profile_image = FileField("Profile image", validators=[FileAllowed(["jpg", "png"])])
    name = StringField("Name", validators=[DataRequired("name cannot be empty.")])
    email = StringField(
        "Email",
        validators=[
            DataRequired("Email cannot be empty."),
            Email("Should be a valid email"),
        ],
    )
    address = StringField(
        "Permanent Address", validators=[DataRequired("Address is required.")]
    )
    contact_number = StringField(
        "Contact number", validators=[DataRequired("Contact number is required")]
    )

    def validate_contact(self):
        if len(self.contact_number) != 11 or not self.contact_number.isnumeric():
            raise ValidationError("Please enter a valid contact number")

    submit = SubmitField("Update")
