""":mod:`soran.web.response` --- soran API response functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import jsonify

__all__ = 'ok', 'created',

def ok(message='', **kwargs):
    """Return 200 response.
    """
    return jsonify(message=message, data=kwargs), 200


def created(message='', **kwargs):
    """Return 201 response.
    """
    return jsonify(message=message, data=kwargs), 201
