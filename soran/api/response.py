""":mod:`soran.api.response` --- soran API response functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import date, datetime
from functools import singledispatch
import json

from flask import Response
from werkzeug.exceptions import HTTPException

from ..user import User


__all__ = (
    'APIError', 'APIBadRequest', 'APIIntegrityError',
    'json_result', 'jsonable',
)


class APIError(HTTPException):

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    def get_body(self, environ=None):
        return json.dumps({'message': self.description,
                           'status_code': self.code,
                           'data': {}})


class APIIntegrityError(APIError):

    code = 500


class APIBadRequest(APIError):

    code = 400


def json_result(data=None, status=200, **kwargs) -> Response:
    result = data or kwargs
    payload = {'message': '', 'data': result, 'status_code': status}
    return Response(json.dumps(jsonable(payload)),
                    status=status,
                    content_type='application/json')


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
        for item in arg[:]:
            r.append(jsonable(item, depth))
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
            'name': arg.name,
            'service': arg.service,
            'created_at': jsonable(arg.created_at, depth),
            'updated_at': jsonable(arg.updated_at, depth)
        })
    return o


@jsonable.register(datetime)
@jsonable.register(date)
def _(arg, depth=1):
    return arg.strftime('%Y-%m-%dT%H:%M:%S')
