from flask import Blueprint, render_template, abort, request

from music.adapters import repository
from music.tracks.services import get_review_by_rating, get_track_by_id, get_tracks, get_all_tracks, get_tracks_for_search

tracks_blueprint = Blueprint('tracks_bp', __name__)

@tracks_blueprint.route('/browse_tracks')
def browse():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str).strip()
    search_type = request.args.get('search_type', '', type=str)

    if search:
        tracks, current_page, total_pages = get_tracks_for_search(get_all_tracks(repository.repo_instance), page, search, search_type)

    else:
        tracks, current_page, total_pages = get_tracks(repository.repo_instance, page)
    return render_template('browse_tracks.html', tracks=tracks,
        current_page=current_page, total_pages=total_pages, search=search, search_type=search_type)


@tracks_blueprint.route('/track/<int:track_id>')
def track_detail(track_id: int):
    track = get_track_by_id(track_id, repository.repo_instance)
    if track is None:
        abort(404)
    reviews = get_review_by_rating(track, repository.repo_instance)
    return render_template('simple_track.html', track=track, reviews=reviews)
