""":mod:`soran.web.response` --- soran API response functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime, date
from functools import singledispatch

from flask import jsonify

from ..user import User
from .auth import Token

__all__ = 'ok', 'created', 'jsonable'

def ok(message='', depth=2, **kwargs):
    """Return 200 response.

    :param str message: a message
    :param int depth: parse depth of data.
    :return: a response that contain a json.
    """
    return jsonify(message=message, data=jsonable(kwargs, depth)), 200


def created(message='', depth=2, **kwargs):
    """Return 201 response.

    :param str message: a message
    :param int depth: parse depth of data.
    :return: a response that contain a json.
    """
    return jsonify(message=message, data=jsonable(kwargs, depth)), 201


@singledispatch
def jsonable(arg, depth=1):
    return arg


@jsonable.register(dict)
def _(arg, depth=1):
    if depth >= 1:
        depth -= 1
        for k, v in arg.copy().items():
            arg[k] = jsonable(v, depth)
        return arg
    return {}


@jsonable.register(User)
def _(arg, depth=1):
    o = {'id': arg.id}
    if depth >= 1:
        depth -= 1
        o.update({
            'username': arg.username,
            'password': arg.password,
            'service': arg.service,
            'created_at': jsonable(arg.created_at, depth),
            'modified_at': jsonable(arg.modified_at, depth)
        })
    return o


@jsonable.register(datetime)
@jsonable.register(date)
def _(arg, depth=1):
    return arg.strftime('%Y-%m-%dT%H:%M:%S')


@jsonable.register(Token)
def _(arg, depth=1):
    return arg.token
