class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATION = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///placement.sqlite3"
    SECRET_KEY = "1$1xJEtqo7x1fu9zci$"
