import os

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pytest_factoryboy import register
from sqlalchemy.orm import scoped_session

from app import create_app
from app.extensions.database.sqlalchemy import db as _db
from tests.seeder.conftest import model_factories


@pytest.fixture(scope="session")
def app() -> Flask:
    app = create_app("testing")
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db(app: Flask):
    database_url = app.config["SQLALCHEMY_DATABASE_URI"]

    _is_local_db_used(database_url)

    _db.app = app

    if is_sqlite_used(database_url):
        _db.create_all()
        yield _db
        _db.drop_all()
    else:
        yield _db


def is_sqlite_used(database_url: str):
    if ":memory:" in database_url:
        return True
    return False


def _is_local_db_used(database_url: str):
    """
    local db를 사용하면 memory db 삭제
    """
    if ":memory:" not in database_url:
        if os.path.exists(database_url.split("sqlite:///")[-1]):  # :memory:
            os.unlink(database_url.split("sqlite:///")[-1])


@pytest.fixture(scope="function")
def session(db: SQLAlchemy) -> scoped_session:
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db._make_scoped_session(options=options)

    db.session = session

    set_factories_session(session)

    yield db.session

    transaction.rollback()
    connection.close()
    session.remove()


def register_factories():
    # 예시) register(StoreFactory) 이런 형태
    for factory in model_factories:
        register(factory)


register_factories()


def set_factories_session(session):
    # 예시) UserFactory._meta.sqlalchemy_session = session
    for factory in model_factories:
        factory._meta.sqlalchemy_session = session
        # factory._meta.sqlalchemy_session_persistence = 'flush'
