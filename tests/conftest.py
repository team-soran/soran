import contextlib

from flask import g
from pytest import fixture
from sqlalchemy import create_engine

from boilerplate.db import Base, Session
from boilerplate.web.app import app

TEST_DATABASE_URL = 'sqlite:///test.db'

def get_engine():
    url = app.config['DATABASE_URL'] = TEST_DATABASE_URL
    engine = create_engine(url)
    app.config['DATABASE_ENGINE'] = engine
    return engine


@contextlib.contextmanager
def get_session():
    engine = get_engine()
    try:
        metadata = Base.metadata
        metadata.drop_all(engine)
        metadata.create_all(engine)
        session = Session(bind=engine)
        yield session
        session.rollback()
        metadata.drop_all(engine)
    finally:
        engine.dispose()


@fixture
def f_session():
    with get_session() as sess, app.test_request_context() as _ctx:
        _ctx.push()
        setattr(g, 'sess', sess)
        return sess
