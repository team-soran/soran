""":mod:`soran.web.auth` --- auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime, timedelta

from flask import current_app, json
from itsdangerous import JSONWebSignatureSerializer

from ..db import session
from ..user import User

__all__ = 'Token',

class Token:
    EXPIRED_DAYS = 1000

    def __init__(self, user, expired_at=None):
        if expired_at is None:
            expired_at = datetime.now() + timedelta(days=self.EXPIRED_DAYS)
        self.expired_at = expired_at
        self.user = user

    @classmethod
    def get_serializer(cls):
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

    @property
    def token(self):
        """Create a token from given :class:`soran.user.User`

        :return: a generated token.
        :rtype: str
        """
        if not self.user:
            return None
        s = Token.get_serializer()
        return s.dumps({'user_id': self.user.id}).decode('utf-8')

    @classmethod
    def validate(cls, tok):
        """Find a user from given token.

        :param :class:`Token` token: a generated soran token.
        :return: a user.
        :rtype: :class:`soran.user.User`
        """
        s = Token.get_serializer()
        payload = s.loads(tok)
        user = session.query(User)\
                      .filter(User.id == payload['user_id'])\
                      .first()
        return user

    def __eq__(self, other):
        return self.token == other and self.user.id == Token.validate(other).id
