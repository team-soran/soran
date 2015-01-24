from pytest import fixture

from soran.user import User
from soran.web.auth import soran_token

@fixture
def f_user(f_session):
    user = User(username='hello', password='password:hello', service='naver')
    f_session.add(user)
    f_session.commit()
    return user


def test_make_token(f_user):
    token = soran_token(f_user)
    assert token


def test_find_user_from_token(f_user):
    user = soran_token(soran_token(f_user))
    assert user == f_user
