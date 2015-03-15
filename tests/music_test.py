from soran.music import Music


def test_create_music(f_session):
    music_name = 'christmalo.win'
    album = 'Quiet Night'
    artist = 'Seotaiji'
    music = Music(name=music_name, album=album, artist=artist)
    f_session.add(music)
    f_session.commit()
    find_music = f_session.query(Music)\
        .filter(Music.name == music_name)\
        .first()
    assert find_music