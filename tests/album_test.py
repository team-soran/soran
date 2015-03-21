from pytest import fixture

from soran.album import Album, AlbumArtistAssoc

from .artist_test import f_artist


def test_create_album(f_session):
    name = 'aaa'
    service = 'naver'
    album = Album(name=name, service=service)
    f_session.add(album)
    f_session.commit()
    find_album = f_session.query(Album) \
                          .filter(Album.name == name) \
                          .first()
    assert find_album
    assert hasattr(find_album, 'id')
    assert find_album.id
    assert hasattr(find_album, 'created_at')
    assert find_album.created_at
    assert hasattr(find_album, 'updated_at')
    assert find_album.updated_at
    assert name == find_album.name
    assert service == find_album.service
    assert hasattr(find_album, 'artists')
    assert hasattr(find_album, 'songs')


def test_create_album_artist_assoc(f_session, f_album, f_artist):
    album_artist_assoc = AlbumArtistAssoc(album=f_album, artists=f_artist)
    f_session.add(album_artist_assoc)
    f_session.commit()
    find_album_assoc = f_session.query(AlbumArtistAssoc) \
                                .filter(AlbumArtistAssoc.album_id == f_album.id) \
                                .first()
    find_artist_assoc = f_session.query(AlbumArtistAssoc) \
                                 .filter(AlbumArtistAssoc.artist_id == f_artist.id) \
                                 .first()
    assert find_album_assoc
    assert find_artist_assoc
    assert album_artist_assoc
    assert f_album.id == album_artist_assoc.album_id
    assert f_artist.id == album_artist_assoc.artist_id


@fixture
def f_album():
    name = 'aaa'
    service = 'naver'
    return Album(name=name, service=service)
