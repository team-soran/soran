""":mod:`soran.web.user` --- soran user API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint, jsonify, request, abort, current_app
from sqlalchemy.exc import IntegrityError

from ..db import session
from ..user import User
from .auth import soran_token
from .response import ok, created

bp = Blueprint('user', __name__, template_folder='templates/user')

@bp.route('/', methods=['POST'])
def create():
    """Create a user.
    """
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    service = request.form.get('service', None)
    if username is None or password is None or service is None:
        abort(400)
    user = User(name=username, password=password, service=service)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        current_app.logger.error(exc)
        abort(500)
    return created()


@bp.route('/authorize/', methods=['POST'])
def authorize():
    """Authorize a user and return a token.
    """
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    secret_key = current_app.config.get('SECRET_KEY', ':)')
    if username is None or password is None:
        abort(400)
    user = session.query(User)\
           .filter(User.username == username)\
           .filter(User.password == password)\
           .first()
    if not user:
        abort(404)
    return ok(token=soran_token(user))
