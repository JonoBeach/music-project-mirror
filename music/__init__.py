"""Initialize Flask app."""

from flask import Flask, render_template

# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from music.domainmodel.track import Track


# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_track():
    some_track = Track(1, "Heat Waves")
    some_track.track_duration = 250
    some_track.track_url = 'https://spotify/track/1'
    return some_track


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_bp)

    return app
