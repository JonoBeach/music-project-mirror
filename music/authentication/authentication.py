from flask import Blueprint, render_template, redirect, url_for, session

from password_validator import PasswordValidator

import music.authentication.services as services

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

# setup blueprint
authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_error_message = None

    if form.validate_on_submit():
        try:
            #TODO: adding user, requires data repository
            #services.add_user(form.username.data, form.password.data, repo.repo_instance)

            # success in registration
            return redirect(url_for('authentication_bp.login'))

        # if username is already taken
        except:
            username_error_message = 'This username has already been taken, please choose another'

    # for GET or failed POST, return registration page
    return render_template(
        'authentication/credentials.html',
        form=form,
        title="register",
        username_error_message=username_error_message,
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_error_message = None

    if form.validate_on_submit():
        # username and password have passed validation checking
        # lookup user and authenticate them
        try:
            #TODO: ----------- Need to implement the auth service layer for these things --------------
            #TODO: get user details
            #user = services.get_user(form.username.data, repo.repo_instance)

            #TODO: authenticate user
            #services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            #TODO: create user session
            #session.clear()
            #session['username'] = user['username']

            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            username_error_message = 'There is no account associated with this username'

        except services.UsernameTooShortException:
            username_error_message = 'The username needs to be at least 4 characters'


    # for GET or failed POST, return login page
    return render_template(
        'authentication/credentials.html',
        form=form,
        title="login",
    )

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))

def login_required():
    return redirect(url_for('authentication_bp.login'))


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
    password = PasswordField('password', [
        DataRequired(message='Please enter a password'),
        PasswordValid(),
        EqualTo('confirm', message='Your password confirmation did not match!')])
    confirm = PasswordField('confirm', [
        DataRequired(message='Please enter your password again'), ])
    submit = SubmitField('register')


class LoginForm(FlaskForm):
    username = StringField('username', [
        DataRequired(message='Please enter a username')])
    password = PasswordField('password', [
        DataRequired(message='Please enter a password')])
    confirm = None
    submit = SubmitField('login')
