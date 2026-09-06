"""Initialize Flask app."""

from flask import Flask, render_template

# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from music.domainmodel.track import Track
from music.adapters.memory_repository import MemoryRepository
import music.adapters.repository as repo

# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_track():
    some_track = Track(1, "Heat Waves")
    some_track.track_duration = 250
    some_track.track_url = 'https://spotify/track/1'
    return some_track


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    if test_config is not None:
        # load test config and overwrite normal config
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
        app.debug = True

    repo.repo_instance = MemoryRepository()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_bp)

    # register blueprints
    with app.app_context():
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
