""":mod:`soran.web.user` --- soran user API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import (Blueprint, request, abort, current_app,
                   render_template)
from flask_wtf import Form
from sqlalchemy.exc import IntegrityError
from wtforms import HiddenField, StringField, PasswordField
from wtforms.validators import input_required

from ..db import session
from ..user import User
from .auth import Token
from .response import ok, created


bp = Blueprint('user', __name__, template_folder='templates/user')


class UserForm(Form):

    name = StringField(label='이름', validators=[input_required()])

    who = HiddenField(validators=[input_required()], default='users')

    service = HiddenField(validators=[input_required()], default='soran')


class CreateUserForm(UserForm):

    password = PasswordField(label='비밀번호', validators=[input_required()])


@bp.route('/users/', methods=['POST'])
def create():
    """Create a user.
    """
    form = CreateUserForm()
    if not form.validate_on_submit():
        print(form.errors)
        abort(400)
    user = User()
    form.populate_obj(user)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        current_app.logger.error(exc)
        abort(500)
    return created()


@bp.route('/users/authorize/', methods=['POST'])
def authorize():
    """Authorize a user and return a token.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        abort(400)
    user = session.query(User) \
                  .filter(User.name == username) \
                  .first()
    if not user or user.password != password:
        abort(404)
    return ok(token=Token(user=user, expired_at=None))


@bp.route('/users/authorize/', methods=['GET'])
def get_authroize():
    form = CreateUserForm()
    form.process(request.args)
    return render_template('authroize.html', form=form)
