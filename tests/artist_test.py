from pytest import fixture

from soran.artist import Artist, ArtistSongAssoc

from .song_test import f_song


def test_create_artist(f_session):
    name = 'aaa'
    service = 'naver'
    artist = Artist(name=name, service=service)
    f_session.add(artist)
    f_session.commit()
    find_artist = f_session.query(Artist) \
                           .filter(Artist.name == name) \
                           .first()
    assert find_artist
    assert hasattr(find_artist, 'id')
    assert find_artist.id
    assert hasattr(find_artist, 'created_at')
    assert find_artist.created_at
    assert hasattr(find_artist, 'updated_at')
    assert find_artist.updated_at
    assert name == find_artist.name
    assert service == find_artist.service
    assert hasattr(find_artist, 'songs')


def test_create_artist_song_assoc(f_session, f_artist, f_song):
    artist_song_assoc = ArtistSongAssoc(artists=f_artist, songs=f_song)
    f_session.add(artist_song_assoc)
    f_session.commit()
    assert artist_song_assoc
    assert f_artist.id == artist_song_assoc.artist_id
    assert f_song.id == artist_song_assoc.song_id


@fixture
def f_artist():
    name = 'aaa'
    service = 'naver'
    return Artist(name=name, service=service)