from flask import g
from pytest import fixture
from sqlalchemy import create_engine

from soran.album import Album
from soran.artist import Artist
from soran.db import Base, Session
from soran.user import User
from soran.web.app import app


TEST_DATABASE_URL = 'sqlite:///test.db'


def get_engine():
    url = app.config['DATABASE_URL'] = TEST_DATABASE_URL
    engine = create_engine(url)
    app.config['DATABASE_ENGINE'] = engine
    return engine


@fixture
def f_app():
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )
    return app


@fixture
def f_user(f_session):
    user = User(name='hello', password='password:hello', service='naver')
    f_session.add(user)
    f_session.commit()
    return user


@fixture
def f_album(f_session):
    name = 'Where is leeSA?'
    service = 'naver'
    album = Album(name=name, service=service)
    f_session.add(album)
    f_session.commit()
    return album


@fixture
def f_artist(f_session):
    name = 'leeSA'
    service = 'naver'
    artist = Artist(name=name, service=service)
    f_session.add(artist)
    f_session.commit()
    return artist
'''
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
'''

@fixture
def f_session(f_app, request):
    with f_app.test_request_context() as _ctx:
        engine = get_engine()
        Base.metadata.create_all(engine)
        _ctx.push()
        session = Session(bind=engine)
        f_app.config['TESTING'] = True
        setattr(g, 'sess', session)
        def finish():
            session.close()
            Base.metadata.drop_all(engine)
            engine.dispose()

        request.addfinalizer(finish)
        return session
