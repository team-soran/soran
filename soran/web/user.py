""":mod:`soran.web.user` --- soran user API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import abort, current_app, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from ..db import session
from ..user import User
from .auth import Token
from .forms.user import CreateUserForm
from .response import created
from .route import APIBlueprint


bp = APIBlueprint('user', __name__, template_folder='templates/user')


@bp.route('/users/', methods=['POST'], api=True)
def create():
    """Create a user.
    """
    form = CreateUserForm()
    user = User()
    if not form.validate_on_submit():
        abort(400)
    form.populate_obj(user)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        current_app.logger.error(exc)
        abort(500)
    return created(redirect_to=url_for('hello'), user=user)


@bp.route('/users/authorize/', methods=['POST'], api=True)
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
    return created(redirect_to=url_for('hello'),
                   token=Token(user=user, expired_at=None))


@bp.route('/users/authorize/', methods=['GET'])
def get_authroize():
    form = CreateUserForm()
    form.process(request.args)
    return render_template('authroize.html', form=form)
