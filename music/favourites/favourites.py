from flask import Blueprint, render_template, session, redirect, url_for, request
from music.authentication.authentication import login_required

import music.adapters.repository as repository

from music.favourites.services import remove_favourite

from music.authentication.services import UnknownUserException
favourites_blueprint = Blueprint("favourites_bp", __name__)

@favourites_blueprint.route('/favourites', methods=['GET', 'POST'])
@login_required
def favourites():
    user = repository.repo_instance.get_user(session['username'])

    if user is None:
        return redirect(url_for('home_bp.home'))

    if request.method == 'POST':
        track_id = int(request.form.get('track_id'))
        favourite = next((favourite for favourite in user.favourites if favourite.track.track_id == track_id), None)

        if favourite:
            remove_favourite(user, favourite)

    print(user.favourites)
    return render_template(
        'favourites.html',
        user=user,
        favourite_tracks = [favourite.track.track_id for favourite in user.favourites]
    )
