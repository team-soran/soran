""":mod:`soran.web.response` --- soran API response functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from contextlib import contextmanager
from datetime import date, datetime
from functools import partial, singledispatch

from annotation.typed import optional, typechecked, union
from flask import (Response, abort, flash, jsonify, redirect, render_template,
                   request)

from ..user import User
from .auth import Token
from .route import API_ENDPOINT


__all__ = 'ok', 'created', 'jsonable',


class UnacceptableSoranRequest(Exception):
    """Raise :class:`~DynamicResponse` is unavailable."""

    pass


class DynamicResponse:
    """Create appropriate HTTP response.

    :param str template_name:
    :param int status_code:
    :param list json_fields:
    :param int json_depth:
    :param str message:

    """

    #: Support mimetype.
    mimetype = {
        'html': 'text/html',
        'json': 'application/json'
    }

    #: Available status codes of HTTP response
    available_status_codes = [
        100,  # Continue
        101,  # Switching Protocols
        200,  # OK
        201,  # Created
        202,  # Accepted
        203,  # Non-Authoritative Information
        204,  # No Content
        205,  # Reset Content
        206,  # Partial Content
        300,  # Multiple Choices
        301,  # Moved Permanently
        302,  # Found
        303,  # See Other
        304,  # Not Modified
        305,  # Use Proxy
        307,  # Temporary Redirect
        400,  # Bad Request
        401,  # Unauthorized
        402,  # Payment Required
        403,  # Forbidden
        404,  # Not Found
        405,  # Method Not Allowed
        406,  # Not Acceptable
        407,  # Proxy Authentication Required
        408,  # Request Time-out
        409,  # Conflict
        410,  # Gone
        411,  # Length Required
        412,  # Precondition Failed
        413,  # Request Entity Too Large
        414,  # Request-URI Too Large
        415,  # Unsupported Media Type
        416,  # Requested range not satisfiable
        417,  # Expectation Failed
        500,  # Internal Server Error
        501,  # Not Implemented
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Time-out
        505,  # HTTP Version not supported
    ]

    @typechecked
    def __init__(self, template_name: optional(str)=None,
                 status_code: optional(int)=None,
                 json_fields: union(tuple, list)=None,
                 json_depth: optional(int)=2, message: str='',
                 *args, **kwargs):
        if status_code not in self.available_status_codes:
            raise ValueError('Invalid status code: {}'.format(status_code))
        self.template_name = template_name
        self.status_code = status_code
        self.json_fields = json_fields
        self.json_depth = json_depth
        self.message = message
        self.args = args
        self.kwargs = kwargs

    @typechecked
    def redirect(self, *args, **kwargs) -> Response:
        """Redirect to given url."""
        return redirect(args[0], code=kwargs.get('code', 302))

    @property
    def response(self) -> Response:
        """Create a response.

        It provide various response depends on given argument. if you want to
        return a response, then create :class:`~DynamicResponse` and
        call :attr:`DynamicResponse.response` .

        .. code-block:: python

           def make_response(...):
               dr = DynamicResponse(...)
               return dr.response

        """
        with self._request_context(
                self.template_name, self.status_code, self.json_fields,
                self.json_depth, self.message) as resp:
            return resp(*self.args, **self.kwargs)

    @typechecked
    @contextmanager
    def _request_context(self, template_name: optional(str)=None,
                         status_code: optional(int)=None,
                         json_fields: union(list, tuple)=None,
                         json_depth: int=2,
                         message: str=''):
        """Create request context which provide appropriate response fucntion.

        :param str template_name:
        :param int status_code:
        :param list json_fields:
        :param int json_depth:
        :param str message:
        :return:
        """
        response = None
        if str(status_code).startswith('3'):
            response = partial(self.redirect, code=302)
        elif self._is_html_request():
            response = partial(self._html_response, template_name, status_code,
                               message)
        elif self._is_json_request():
            response = partial(self._json_response, status_code, json_fields,
                               json_depth, message)
        if not response:
            raise UnacceptableSoranRequest()
        yield response

    def _html_response(self, template_name, status_code, flash_message,
                       *args, **kwargs):
        """Return html response.

        :param template_name:
        :param status_code:
        :param flash_message:
        :param args:
        :param kwargs:
        :return:
        """
        if flash_message:
            flash(flash_message)
        # FIXME 40x, 50x 는 멋진 에러페이지 만들어서 처리하기
        response = None
        status_stat = int(status_code / 100)
        if (status_code == 400 and template_name) or status_code == 200:
            response = (
                render_template(template_name, **kwargs),
                status_code
            )
        elif status_code == 201:
            response = self.redirect(template_name, code=302)
        elif status_stat == 4 or status_stat == 5:
            abort(status_code)
        else:
            response = render_template(template_name, *args, **kwargs)
        return response

    def _json_response(self, status_code, select_fields, depth, message,
                       *args, **kwargs):
        """Return json response.

        :param status_code:
        :param select_fields:
        :param depth:
        :param message:
        :param args:
        :param kwargs:
        :return:
        """
        data = jsonable(args, depth) if args else jsonable(kwargs, depth)
        return (
            jsonify(message=message,
                    data=data),
            status_code
        )

    def _is_html_request(self):
        return self._find_request_context() == self.mimetype['html']

    def _is_json_request(self):
        return self._find_request_context() == self.mimetype['json']

    def _find_request_context(self):
        if API_ENDPOINT in request.url_rule.endpoint:
            return self.mimetype['json']
        return self.mimetype['html']


def ok(template_name=None, message='', depth=2, fields=[], **kwargs):
    """Return 200 response.

    :param str message: a message
    :param int depth: parse depth of data.
    :return: a response that contain a json.
    """
    dr = DynamicResponse(
        template_name, 200, fields, depth, message, **kwargs)
    return dr.response


def created(template_name=None, redirect_to=None, message='', depth=2,
            fields=[], **kwargs):
    """Return 201 response.

    :param str message: a message
    :param int depth: parse depth of data.
    """
    dr = DynamicResponse(
        template_name or redirect_to, 201, fields, depth, message, **kwargs)
    return dr.response


def bad_syntax(template_name=None, message='', depth=2, fields=[], **kwargs):
    dr = DynamicResponse(
        template_name, 400, fields, depth, message, **kwargs)
    return dr.response


def internal_server_error(template_name=None, message='', depth=2,
                          fields=[], **kwargs):
    """Return Internal server error.

    :param template_name:
    :param message:
    :param depth:
    :param fields:
    :param kwargs:
    :return:
    """
    dr = DynamicResponse(
        template_name, 500, fields, depth, message, **kwargs
    )
    return dr.response


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


@jsonable.register(Token)
def _(arg, depth=1):
    return arg.token
