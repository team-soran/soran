from pytest import fixture, yield_fixture
from sqlalchemy import create_engine

from soran.album import Album
from soran.artist import Artist
from soran.db import Base, Session
from soran.song import Song
from soran.user import User
from soran.web.app import app


TEST_DATABASE_URL = 'sqlite:///test.db'


def get_engine():
    url = app.config['DATABASE_URL'] = TEST_DATABASE_URL
    engine = create_engine(url)
    app.config['DATABASE_ENGINE'] = engine
    return engine


@fixture
def f_app(f_session):
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        DATABASE_URL=TEST_DATABASE_URL
    )
    return app


@fixture
def f_user(f_session):
    user = User(name='hello', password='password:hello', service='naver')
    f_session.add(user)
    f_session.commit()
    return user


@fixture
def f_song(f_session, f_album):
    song = Song(name='Could stop that smile?',
                service='naver',
                album=f_album)
    f_session.add(song)
    f_session.commit()
    return song


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


@yield_fixture
def f_session():
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
