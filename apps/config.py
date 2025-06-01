import os
import random
import string


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice(string.ascii_lowercase)
                             for i in range(32))

    # Social AUTH context
    SOCIAL_AUTH_GITHUB = False

    GITHUB_ID = os.getenv('GITHUB_ID', None)
    GITHUB_SECRET = os.getenv('GITHUB_SECRET', None)

    # Enable/Disable Github Social Login
    if GITHUB_ID and GITHUB_SECRET:
        SOCIAL_AUTH_GITHUB = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE = 'postgresql'
    DB_USERNAME = 'raihcita'
    DB_PASS = 'WuB5I8yXtGELcL46mC5xDWJxEAux1LwR'
    DB_HOST = 'dpg-d0u1v9adbo4c73abdg70-a'
    DB_PORT = '5432'
    DB_NAME = 'raihcita'

    USE_SQLITE = True

    # try to set up a Relational DBMS
    if DB_ENGINE and DB_NAME and DB_USERNAME:

        try:

            # Relational DBMS: PSQL, MySql
            SQLALCHEMY_DATABASE_URI = "postgresql://raihcita:WuB5I8yXtGELcL46mC5xDWJxEAux1LwR@dpg-d0u1v9adbo4c73abdg70-a.frankfurt-postgres.render.com/raihcita"

            # SQLALCHEMY_DATABASE_URI = "postgresql://raihcita:WuB5I8yXtGELcL46mC5xDWJxEAux1LwR@dpg-d0u1v9adbo4c73abdg70-a.frankfurt-postgres.render.com/raihcita"

            USE_SQLITE = False

        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e))
            print('> Fallback to SQLite ')

    if USE_SQLITE:

        # This will create a file in <app> FOLDER
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
            os.path.join(basedir, 'db.sqlite3')


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
