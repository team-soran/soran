""":mod:`soran.api.response` --- soran API response functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import json
from datetime import date, datetime
from functools import singledispatch
from flask import Response

from ..user import User


def json_result(**kwargs):
    return Response(json.dumps(jsonable(kwargs)), mimetype='application/json')


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

