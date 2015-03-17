from soran.song import Song


def test_create_song(f_session):
    name = 'aaa'
    service = 'naver'
    song = Song(name=name, service=service)
    f_session.add(song)
    f_session.commit()
    find_artist = f_session.query(Song)\
        .filter(Song.name == name)\
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
