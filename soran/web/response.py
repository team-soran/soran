""":mod:`soran.web.response` --- soran API response functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime, date
from functools import singledispatch

import json

from flask import jsonify as flask_jsonify

from ..user import User

__all__ = 'ok', 'created', 'jsonify'

def ok(message='', **kwargs):
    """Return 200 response.
    """
    return flask_jsonify(message=message, data=kwargs), 200


def created(message='', **kwargs):
    """Return 201 response.
    """
    return flask_jsonify(message=message, data=kwargs), 201


@singledispatch
def jsonify(arg):
    return json.dumps(arg)


@jsonify.register(User)
def _(arg):
    o = {
        'id': arg.id,
        'username': arg.username,
        'password': arg.password,
        'service': arg.service,
        'created_at': jsonify(arg.created_at),
        'modified_at': jsonify(arg.modified_at)
    }
    return jsonify(o)


@jsonify.register(datetime)
@jsonify.register(date)
def _(arg):
    return arg.strftime('%Y-%m-%dT%H:%M:%S')
