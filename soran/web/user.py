""":mod:`soran.web.user` --- soran user API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import (Blueprint, current_app, render_template, request,
                   redirect, url_for)
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from ..db import session
from ..user import User
from .forms.user import CreateUserForm, AuthorizeForm


bp = Blueprint('user', __name__, template_folder='templates/user',
               url_prefix='/users')


@bp.route('/', methods=['POST'])
def create():
    """Create a user.
    """
    form = CreateUserForm(request.form)
    if not form.validate():
        # FIXME response.py에서 400 담당하는 render함수만들기
        return render_template('authorize.html', form=form), 400
    user = User()
    form.populate_obj(user)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        current_app.logger.error(exc)
        # FIXME 예쁜 500만들기
        raise InternalServerError()
    return redirect(url_for('hello'))


@bp.route('/authorize/', methods=['POST'])
def authorize():
    """Authorize a user and return a token.
    """
    form = AuthorizeForm(formdata=request.form)
    if not form.validate():
        # FIXME response.py에서 400 담당하는 render함수만들기
        return render_template('authorize.html', form=form), 400
    return redirect(url_for('hello'))


@bp.route('/authorize/', methods=['GET'])
def get_authroize():
    form = CreateUserForm(request.args)
    return render_template('authorize.html', form=form)
