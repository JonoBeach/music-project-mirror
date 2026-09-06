from flask import Blueprint, render_template, abort

from music.domainmodel import track
from music.tracks.services import get_track_by_id, get_tracks


tracks_blueprint = Blueprint('tracks_bp', __name__)

@tracks_blueprint.route('/browse_tracks')
def browse():
    tracks = get_tracks()
    return render_template('browse_tracks.html', tracks=tracks)

@tracks_blueprint.route('/track/<int:track_id>')
def track_detail(track_id: int):
    track = get_track_by_id(track_id)
    if track is None:
        abort(404)
    return render_template('simple_track.html', track=track)
