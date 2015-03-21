""":mod:`soran.web.user` --- soran user API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import (Blueprint, jsonify, request, abort, current_app,
                   render_template)
from sqlalchemy.exc import IntegrityError

from ..db import session
from ..user import User, Password
from .auth import Token
from .response import ok, created


bp = Blueprint('user', __name__, template_folder='templates/user')


@bp.route('/', methods=['POST'])
def create():
    """Create a user.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    service = request.form.get('service')
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
    username = request.form.get('username')
    password = request.form.get('password')
    secret_key = current_app.config.get('SECRET_KEY', ':)')
    if username is None or password is None:
        abort(400)
    user = session.query(User)\
           .filter(User.name == username)\
           .first()
    if not user or user.password != password:
        abort(404)
    return ok(token=Token(user=user, expired_at=None))


@bp.route('/authorize/', methods=['GET'])
def get_authroize():
    return render_template('authroize.html')
