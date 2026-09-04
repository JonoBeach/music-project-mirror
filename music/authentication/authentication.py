from flask import Blueprint, render_template, redirect, url_for, session

from password_validator import PasswordValidator

import music.authentication.services as services

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

# setup blueprint
authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')

#TODO: register route & form
@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            #TODO: adding user
            return redirect(url_for('authentication_bp.login'))

        # if username is already taken
        except:
            pass

    # for GET or failed POST, return registration page
    return render_template(
        'authentication/credentials.html',
        form=form,
        title="register",
    )

#TODO: login route & form
@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # username and password have passed validation checking
        try:
            #TODO: get user details
            #TODO: authenticate user
            #TODO: create user session
            return redirect(url_for('home_bp.home')) #TODO: home bp not implemented yet

        except:
            pass

    # for GET or failed POST, return login page
    return render_template(
        'authentication/credentials.html',
        form=form,
        title="login",
    )

#TODO: logout route & functionality
@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = 'Your password must be at least 8 characters, contain no spaces, contain an upper-case, lower-case, and a digit!'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()

        schema \
            .min(8)\
            .has().uppercase()\
            .has().lowercase()\
            .has().digits()\
            .has().no().spaces()\

        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('username', [
                           DataRequired(message='Please input a username!'),
                           Length(min=4, message='Your username is too short!')])
    password = PasswordField('password', [DataRequired(message='Please enter a password'), PasswordValid(), EqualTo('confirm', message='Your password confirmation did not match!')])
    confirm = PasswordField('confirm', [DataRequired(message='Please enter your password again'), ])
    submit = SubmitField('register')


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    confirm = None
    submit = SubmitField('login')
