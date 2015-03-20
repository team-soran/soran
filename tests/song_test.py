from soran.song import Song
from soran.album import Album
from soran.artist import Artist

from pytest import fixture


def test_create_song(f_session):
    name = 'aaa'
    service = 'naver'
    song = Song(name=name, service=service)
    f_session.add(song)
    f_session.commit()
    find_song = f_session.query(Song) \
                         .filter(Song.name == name) \
                         .first()
    assert find_song
    assert hasattr(find_song, 'id')
    assert find_song.id
    assert hasattr(find_song, 'created_at')
    assert find_song.created_at
    assert hasattr(find_song, 'updated_at')
    assert find_song.updated_at
    assert name == find_song.name
    assert service == find_song.service
    assert hasattr(find_song, 'album_id')
    assert hasattr(find_song, 'album')


@fixture
def f_song():
    name = 'aaa'
    service = 'naver'
    return Song(name=name, service=service)