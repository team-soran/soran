""":mod:`soran.web.forms.user` --- 사용자와 관계있는 폼들
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy.orm.exc import NoResultFound
from wtforms import HiddenField, PasswordField, StringField, ValidationError
from wtforms.validators import InputRequired

from . import ServiceForm

from soran import User
from soran.db import session


__all__ = 'CreateUserForm', 'UserForm', 'AuthorizeForm',


class UserForm(ServiceForm):
    """사용자 폼"""

    name = StringField(label='이름', validators=[InputRequired()])

    who = HiddenField(validators=[InputRequired()], default='users')


class CreateUserForm(UserForm):
    """회원가입 폼"""

    password = PasswordField(label='비밀번호', validators=[InputRequired()])

    def validate_name(self, name):
        try:
            session.query(User) \
                   .filter_by(name=name.data) \
                   .one()
        except NoResultFound:
            pass
        else:
            raise ValidationError('User(name={}) already exists'
                                  .format(name))


class AuthorizeForm(UserForm):

    password = PasswordField(label='비밀번호', validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super(AuthorizeForm, self).__init__(*args, **kwargs)
        self.user = None

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        super(AuthorizeForm, self).process(formdata, obj, data, **kwargs)

    def validate_name(self, name):
        try:
            self.user = session.query(User) \
                               .filter_by(name=name.data) \
                               .one()
        except NoResultFound:
            raise ValidationError('not found')
        return name

    def validate_password(self, password):
        if not self.user or self.user.password != password.data:
            raise ValidationError('passsword error')
        return password
