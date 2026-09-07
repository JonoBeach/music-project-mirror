"""Initialize Flask app."""

from flask import Flask, render_template

from music.adapters.memory_repository import MemoryRepository
import music.adapters.repository as repo


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
        from .tracks import tracks_blueprint
        app.register_blueprint(authentication.authentication_blueprint)
        app.register_blueprint(tracks_blueprint)

    return app
