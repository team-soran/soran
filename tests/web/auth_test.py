from datetime import datetime

from soran.web.auth import soran_token

def test_make_token(f_user):
    token = soran_token(f_user)
    assert token


def test_find_user_from_token(f_user):
    user = soran_token(soran_token(f_user))
    assert user == f_user


def test_none_token():
    token = soran_token(None)
    assert not token


def test_make_token_with_expired_at(f_user):
    token = soran_token(f_user, expired_at=datetime.now())
    assert token
