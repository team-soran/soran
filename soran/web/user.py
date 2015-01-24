""":mod:`soran.web.user` --- soran user API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint, jsonify, request, abort

from ..db import session
from ..user import User

bp = Blueprint('user', __name__, template_folder='templates/user')

@bp.route('/', methods=['POST'])
def create_user():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    service = request.form.get('service', None)
    if username is None or password is None or service is None:
        abort(400)
    user = User(username=username, password=password, service=service)
    session.add(user)
    session.commit()
    return jsonify()
