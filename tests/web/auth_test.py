from pytest import fixture

from soran.web.auth import Token

def test_create_token(f_user):
    tok = Token(user=f_user)
    assert tok.token
    assert tok.expired_at
    assert Token.validate(tok.token)


@fixture
def f_token(f_user):
    return Token(user=f_user)


def test_make_token(f_token):
    token = f_token.token
    assert token


def test_find_user_from_token(f_user, f_token):
    user = Token.validate(f_token.token)
    assert user == f_user
    assert f_token.token == Token(f_user)


def test_none_token():
    token = Token(None)
    assert not token.token

