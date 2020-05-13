"""App configuration."""
from os import environ


class Config:
    """Set Flask configuration vars from environment variables."""

    # General Config
    SECRET_KEY = "gLPzeNChoL0fl5LdIwVy2xE9wS8t9fxv"
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:////voice.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload and extension
    UPLOAD_FOLDER = 'VoiceReading/static/upload'
    SPEECH_FOLDER = 'VoiceReading/static/speech'
    SPEECH_FOLDER_URL = 'static/speech'
    TTS_FOLDER = 'VoiceReading/static/tts'
    TTS_FOLDER_URL = 'static/tts'
