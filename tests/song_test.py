from soran.song import Song
from .album_test import test_create_album


def test_create_song(f_session):
    name = 'aaa'
    service = 'naver'
    song = Song(name=name, service=service)
    f_session.add(song)
    f_session.commit()
    find_song = f_session.query(Song)\
        .filter(Song.name == name)\
        .first()
    test_create_album(f_session)
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
