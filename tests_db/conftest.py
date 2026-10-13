import pytest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from music.adapters import database_repository
from music.adapters.orm import mapper_registry, map_model_to_tables

TEST_DATA_PATH_DATABASE_LIMITED = Path(__file__).parent / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///:memory:'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    mapper_registry.metadata.create_all(engine)  # Conditionally create database tables.

    map_model_to_tables()

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(bind=engine)

    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.DatabaseRepository(session_factory, True)

    yield engine
    mapper_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(bind=engine)

    yield session_factory
    mapper_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    mapper_registry.metadata.drop_all(engine)
