from soran.archive import Archive

from .user_test import f_user
from .song_test import f_song


def test_create_archive(f_session, f_user, f_song):
    archive = Archive(users=f_user, songs=f_song)
    f_session.add(archive)
    f_session.commit()
    find_archive_user_id = f_session.query(Archive) \
                                    .filter(Archive.user_id == f_user.id) \
                                    .first()
    find_archive_song_id = f_session.query(Archive) \
                                    .filter(Archive.song_id == f_song.id) \
                                    .first()
    assert find_archive_user_id
    assert find_archive_song_id

    assert hasattr(find_archive_user_id, 'id')
    assert hasattr(find_archive_user_id, 'user_id')
    assert hasattr(find_archive_user_id, 'song_id')
    assert hasattr(find_archive_user_id, 'listened_at')
    assert hasattr(find_archive_user_id, 'users')
    assert hasattr(find_archive_user_id, 'songs')

    assert hasattr(find_archive_song_id, 'id')
    assert hasattr(find_archive_song_id, 'user_id')
    assert hasattr(find_archive_song_id, 'song_id')
    assert hasattr(find_archive_song_id, 'listened_at')
    assert hasattr(find_archive_song_id, 'users')
    assert hasattr(find_archive_song_id, 'songs')