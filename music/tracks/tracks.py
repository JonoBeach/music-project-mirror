from flask import Blueprint, render_template, abort, request
from music.tracks.services import get_review_by_rating, get_track_by_id, get_tracks

tracks_blueprint = Blueprint('tracks_bp', __name__)

@tracks_blueprint.route('/browse_tracks')
def browse():
    page = request.args.get('page', 1, type=int)
    tracks, current_page, total_pages = get_tracks(page)
    return render_template('browse_tracks.html', tracks=tracks,
        current_page=current_page, total_pages=total_pages)

@tracks_blueprint.route('/track/<int:track_id>')
def track_detail(track_id: int):
    track = get_track_by_id(track_id)
    if track is None:
        abort(404)
    reviews = get_review_by_rating(track)
    return render_template('simple_track.html', track=track, reviews=reviews)
