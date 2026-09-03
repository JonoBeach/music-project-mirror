from flask import Blueprint, render_template

import music.authentication.services as services

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

# setup blueprint
authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')

#TODO: register route & form
@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    return render_template(
        'authentication/credentials.html',
        form=form,
    )

#TODO: login route & form
@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template(
        'authentication/credentials.html',
        form=form,
    )

#TODO: logout route & functionality


class RegistrationForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('register')


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('login')
