from soran.artist import Artist


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