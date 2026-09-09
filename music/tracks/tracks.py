import time
from flask import Blueprint, render_template, abort, request, session, redirect, url_for

from music.tracks.services import get_review_by_rating, get_track_by_id, get_tracks, get_all_tracks, get_tracks_for_search, add_review, remove_review
from music.favourites.services import add_favourite, remove_favourite

import music.adapters.repository as repository

from flask_wtf import FlaskForm
from wtforms import SubmitField

tracks_blueprint = Blueprint('tracks_bp', __name__)

@tracks_blueprint.route('/browse_tracks', methods=['GET', 'POST'])
def browse():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str).strip()
    search_type = request.args.get('search_type', '', type=str)

    if search:
        tracks, current_page, total_pages = get_tracks_for_search(get_all_tracks(), page, search, search_type)

    else:
        tracks, current_page, total_pages = get_tracks(page)


    if request.method == 'POST':
        try:
            user = repository.repo_instance.get_user(session['username'])
        except KeyError:
            return redirect(url_for('authentication_bp.login'))

        track_id = int(request.form.get('track_id'))

        if request.form.get('action') ==  "Add to favourites":
            track = get_track_by_id(track_id)
            if track is not None:
                add_favourite(user, track)

        elif request.form.get('action') ==  "Remove from favourites":
            favourite = next((favourite for favourite in user.favourites if favourite.track.track_id == track_id), None)

            if favourite:
                remove_favourite(user, favourite)

    # tries getting user, but if it runs into a key error, that means that user is not logged in, so just passes
    favourite_tracks = []
    try:
        user = repository.repo_instance.get_user(session['username'])
        if user is not None:
            favourite_tracks = [favourite.track.track_id for favourite in user.favourites]
    except KeyError:
        favourite_tracks = []

    return render_template('browse_tracks.html', tracks=tracks,
        current_page=current_page, total_pages=total_pages, search=search, search_type=search_type, favourite_tracks=favourite_tracks)


@tracks_blueprint.route('/track/<int:track_id>', methods=['GET', 'POST'])
def track_detail(track_id: int):
    if request.method == 'POST':
        # authentication
        try:
            user = repository.repo_instance.get_user(session['username'])
        except KeyError:
            return redirect(url_for('authentication_bp.login'))

        # favourites
        if request.form.get('action') ==  "Add to favourites":
            track = get_track_by_id(track_id)
            if track is not None:
                add_favourite(user, track)

        elif request.form.get('action') ==  "Remove from favourites":
            favourite = next((favourite for favourite in user.favourites if favourite.track.track_id == track_id), None)

            if favourite is not None:
                remove_favourite(user, favourite)

        # reviews
        if request.form.get('action') ==  "Add review":
            track = get_track_by_id(track_id)
            rating = int(request.form.get('rating'))
            review_text = request.form.get('review')
            date = int(time.time())
            add_review(user, track, rating, review_text, date)

    # tries getting user, but if it runs into a key error, that means that user is not logged in, so just passes
    favourite_tracks = []
    try:
        user = repository.repo_instance.get_user(session['username'])
        if user is not None:
            favourite_tracks = [favourite.track.track_id for favourite in user.favourites]
    except KeyError:
        favourite_tracks = []

    track = get_track_by_id(track_id)
    if track is None:
        abort(404)
    reviews = get_review_by_rating(track)
    return render_template('simple_track.html', track=track, reviews=reviews, favourite_tracks=favourite_tracks)


class RemoveFavouriteForm(FlaskForm):
    submit = SubmitField('Remove from favourites')


class AddFavouriteForm(FlaskForm):
    submit = SubmitField('Add to favourites')
