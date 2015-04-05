""":mod:`soran.web.response` --- soran API response functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime, date
from contextlib import contextmanager
from functools import singledispatch, partial

from flask import jsonify, request, flash, render_template

from ..user import User
from .auth import Token
from .route import API_PREFIX


__all__ = 'ok', 'created', 'jsonable',


class UnacceptableSoranRequest(Exception):
    pass


class DynamicResponse:

    def __init__(self, html_func, status_code=None,
                 html_flash=None, json_fields=None, json_depth=2,
                 json_message='', *args, **kwargs):
        with self._request_context(
                html_func, status_code, html_flash, json_fields, json_depth,
                json_message) as resp:
            return resp(*args, **kwargs)

    @contextmanager
    def _request_context(self, html_func, status_code=None,
                         html_flash=None, json_fields=None, json_depth=2,
                         json_message=''):
        if self._is_html_request():
            return partial(self._html_response, html_func, status_code,
                           html_flash)
        elif self._is_json_request():
            return partial(self._json_response, status_code, json_fields,
                           json_depth, json_message)
        raise UnacceptableSoranRequest()

    def _html_response(self, func, status_code, flash_message,
                       *args, **kwargs):
        if flash_message:
            flash(flash_message)
        return func(*args, **kwargs), status_code

    def _json_response(self, status_code, select_fields, depth, message,
                       *args, **kwargs):
        data = jsonable(args, depth) if args else jsonable(kwargs, depth)
        return (
            jsonify(message=message,
                    data=data),
            status_code
        )


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


@jsonable.register(list)
@jsonable.register(tuple)
def _(arg, depth=1):
    depth -= 1
    r = []
    if depth >= 1:
        depth -= 1
        for item in arg.copy():
            r.append(jsonable(item, depth))
        return arg
    return r


@jsonable.register(dict)
def _(arg, depth=1):
    r = {}
    if depth >= 1:
        depth -= 1
        for k, v in arg.copy().items():
            r[k] = jsonable(v, depth)
        return r
    return r


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
