from flask import Blueprint, render_template, session, redirect, url_for
from music.authentication.authentication import login_required

from music.adapters.repository import repo_instance

from music.authentication.services import get_user, UnknownUserException
favourites_blueprint = Blueprint("favourites_bp", __name__)

@favourites_blueprint.route('/favourites', methods=['GET'])
@login_required
def favourites():
    try:
        user=get_user(session['username'], repo_instance)
    except UnknownUserException:
        return redirect(url_for('home_bp.home'))

    return render_template(
        'favourites.html',
        user=get_user(session['username'], repo_instance)
    )
