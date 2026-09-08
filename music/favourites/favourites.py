from flask import Blueprint, render_template, session, redirect, url_for
from music.authentication.authentication import login_required

from music.adapters.repository import repo_instance

from music.authentication.services import UnknownUserException
favourites_blueprint = Blueprint("favourites_bp", __name__)

@favourites_blueprint.route('/favourites', methods=['GET'])
@login_required
def favourites():
    user = repo_instance.get_user(session['username'])

    if user is None:
        return redirect(url_for('home_bp.home'))

    print(user.favourites)
    return render_template(
        'favourites.html',
        user=user
    )
