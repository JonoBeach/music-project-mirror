"""Initialize Flask app."""

from flask import Flask, render_template

from music.adapters.memory_repository import MemoryRepository
from music.adapters.database_repository import DatabaseRepository
import music.adapters.repository as repo
from music.adapters.orm import mapper_registry, map_model_to_tables

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    if test_config is not None:
        # load test config and overwrite normal config
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
        app.debug = True

    # setup repository
    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = MemoryRepository()
    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']

        database_engine = create_engine(
            database_uri,
            connect_args={"check_same_thread": False},
            poolclass=NullPool,
            echo=database_echo
        )

        # populate database if tables are empty
        should_populate = len(inspect(database_engine).get_table_names()) == 0

        # Create empty tables if they don't exist
        mapper_registry.metadata.create_all(database_engine)

        session_factory = sessionmaker(bind=database_engine)
        map_model_to_tables()
        repo.repo_instance = DatabaseRepository(session_factory, should_populate)

    # register blueprints
    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_bp)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .tracks import tracks_blueprint
        app.register_blueprint(tracks_blueprint)

        from .favourites import favourites
        app.register_blueprint(favourites.favourites_blueprint)

    return app
