""":mod:`soran.web.auth` --- auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime, timedelta
from functools import singledispatch

from flask import current_app, json
from itsdangerous import JSONWebSignatureSerializer

from ..db import session
from ..user import User

__all__ = 'get_serializer', 'soran_token',

EXPIRED_DAYS = 1000

def get_serializer():
    """Get a :class:`itsdangerous.JSONWebSignatureSerializer` .
    """
    default_key = ':)'
    try:
        secret_key = current_app.config.get('SECRET_KEY', default_key)
    except RuntimeError:
        secret_key = default_key
    if secret_key is None:
        secret_key = default_key
    return JSONWebSignatureSerializer(secret_key)


@singledispatch
def soran_token(arg, expired_at=None):
    return arg


@soran_token.register(User)
def _(arg, expired_at=None):
    """Create a token from given :class:`soran.user.User`

    :param soran.user.User arg: a soran user.
    :return: a token.
    :rtype: str
    """
    s = get_serializer()
    if expired_at is None:
        expired_at = datetime.now() + timedelta(days=EXPIRED_DAYS)
    return s.dumps({'user_id': arg.id}).decode('utf-8')


@soran_token.register(bytes)
@soran_token.register(str)
def _(arg, expired_at=None):
    """Find a user from given token.

    :param str arg: a soran token.
    :return: a user.
    :rtype: :class:`soran.user.User`
    """
    s = get_serializer()
    payload = s.loads(arg)
    user = session.query(User)\
           .filter(User.id == payload['user_id'])\
           .first()
    #TODO: Check a expired_at
    return user
