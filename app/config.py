import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "auckland"

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_PRE_PING = True
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": SQLALCHEMY_PRE_PING}

    DEBUG = False
    TESTING = False


class LocalConfig(Config):
    ENV = "local"
    SQLALCHEMY_ECHO = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL") or "sqlite:///:memory:"


class TestConfig(Config):
    ENV = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"

    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL") or "sqlite:///:memory:"


class ProductionConfig(Config):
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL") or "sqlite:///:memory:"


config = {
    "default": LocalConfig,
    "local": LocalConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
