from soran.album import Album


def test_create_album(f_session):
    name = 'aaa'
    service = 'naver'
    album = Album(name=name, service=service)
    f_session.add(album)
    f_session.commit()
    find_album = f_session.query(Album)\
        .filter(Album.name == name)\
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
