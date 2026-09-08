from flask import Blueprint, render_template, session
from music.authentication.authentication import login_required

from music.adapters.repository import repo_instance

from music.authentication.services import get_user
favourites_blueprint = Blueprint("favourites_bp", __name__)

@favourites_blueprint.route('/favourites', methods=['GET'])
#@login_required
def favourites():
    return render_template(
        'favourites.html',
        user=get_user(session['username'], repo_instance)
    )
