from flask import Blueprint, render_template, redirect, url_for, session

from password_validator import PasswordValidator

import music.adapters.repository as repository
import music.authentication.services as services

from functools import wraps

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
            services.add_user(form.username.data, form.password.data, repository.repo_instance)

            # success in registration
            return redirect(url_for('authentication_bp.login'))

        # if username is already taken
        except services.UsernameAlreadyTakenException:
            username_error_message = 'This username has already been taken, please choose another'

    # for GET or failed POST, return registration page
    return render_template(
        'authentication/credentials.html',
        form=form,
        title="Register",
        username_error_message=username_error_message,
        handler_url=url_for('authentication_bp.register'),
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_error_message = None
    password_username_mismatch = None

    if form.validate_on_submit():
        # username and password have passed validation checking
        # lookup user and authenticate them
        try:
            user = services.get_user(form.username.data, repository.repo_instance)

            services.authenticate_user(user['username'], form.password.data, repository.repo_instance)

            session.clear()
            session['username'] = user['username']

            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            username_error_message = 'There is no account associated with this username'

        except services.AuthenticationException:
            password_username_mismatch = 'Your username or password is incorrect, please try again'


    # for GET or failed POST, return login page
    return render_template(
        'authentication/credentials.html',
        form=form,
        title="Login",
        username_error_message=username_error_message,
        password_username_mismatch=password_username_mismatch,
        handler_url=url_for('authentication_bp.login'),
    )

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view

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
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('username', [
        DataRequired(message='Please enter a username')])
    password = PasswordField('password', [
        DataRequired(message='Please enter a password')])
    confirm = None
    submit = SubmitField('Login')
