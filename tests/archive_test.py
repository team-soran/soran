from soran import User, Song

from soran.archive import Archive


def test_create_archive(f_session, f_user, f_song):
    archive = Archive(user=f_user, song=f_song)
    f_session.add(archive)
    f_session.commit()
    assert archive.id
    assert archive.user.id == f_user.id
    assert archive.song.id == f_song.id


def test_create_archive_n_times(f_session, f_album, f_song, f_user):
    data = {'user': [], 'song': []}
    for i in range(0, 10):
        user = User(name='user{}'.format(i),
                    password='password:hello',
                    service='naver')
        f_session.add(user)
        data['user'].append(user)
        song = Song(name='song{}'.format(i),
                    album=f_album,
                    service='naver')
        f_session.add(song)
        data['song'].append(song)
    for user in data['user']:
        f_session.add(Archive(user=user, song=f_song))
    for song in data['song']:
        f_session.add(Archive(song=song, user=f_user))
    f_session.commit()
    # test specific user can listen many songs
    user_archives = f_session.query(Archive) \
                             .join(Archive.song) \
                             .join(Archive.user) \
                             .filter(Archive.user == f_user) \
                             .all()
    song_ids = [song.id for song in data['song']]
    user_ids = [user.id for user in data['user']]
    assert user_archives
    assert len(user_archives) == len(data['song'])
    for user_archive in user_archives:
        assert user_archive.user.id == f_user.id
        assert user_archive.song.id in song_ids
    # test specific song can be listened by many users
    song_archives = f_session.query(Archive) \
                             .join(Archive.song) \
                             .join(Archive.user) \
                             .filter(Archive.song == f_song) \
                             .all()
    assert song_archives
    assert len(song_archives) == len(data['user'])
    for song_archive in song_archives:
        assert song_archive.song.id == f_song.id
        assert song_archive.user.id in user_ids


def test_listens_same_song_over_again(f_session, f_user, f_song):
    n_times = 4
    i = 0
    while i < n_times:
        f_session.add(Archive(user=f_user, song=f_song))
        i += 1
    f_session.commit()
    archives = f_session.query(Archive) \
                        .join(Archive.user) \
                        .join(Archive.song) \
                        .filter(Archive.user == f_user) \
                        .all()
    assert len(archives) == n_times
    for archive in archives:
        assert archive.user.id == f_user.id
        assert archive.song.id == f_song.id
    archives = f_session.query(Archive) \
        .join(Archive.user) \
        .join(Archive.song) \
        .filter(Archive.song == f_song) \
        .all()
    assert len(archives) == n_times
    for archive in archives:
        assert archive.user.id == f_user.id
        assert archive.song.id == f_song.id
