from flask import Blueprint, render_template

import music.authentication.services as services

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')

#TODO: register route & form
@authentication_blueprint.route('/register', methods=['GET', 'POST'])

#TODO: login route & form
@authentication_blueprint.route('/login', methods=['GET', 'POST'])

#TODO: logout route & functionality

class RegistrationForm(FlaskForm):
    #TODO: form details like username, password, and submit
    pass
