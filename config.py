from os import environ
from dotenv import load_dotenv

# load in .env file contents
load_dotenv()


class Config:
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')
    TESTING = environ.get('TESTING')

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    echo = environ.get('SQLALCHEMY_ECHO')
    SQLALCHEMY_ECHO = False
    if echo.lower().strip() == "true":
        SQLALCHEMY_ECHO = True

    REPOSITORY = environ.get('REPOSITORY')
