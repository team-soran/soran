""":mod:`soran.web.forms.user` --- 사용자와 관계있는 폼들
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy.orm.exc import NoResultFound
from wtforms import HiddenField, PasswordField, StringField, ValidationError
from wtforms.validators import InputRequired

from . import ServiceForm

from soran import User
from soran.db import session


__all__ = 'CreateUserForm', 'UserForm',


class UserForm(ServiceForm):
    """사용자 폼"""

    name = StringField(label='이름', validators=[InputRequired()])

    who = HiddenField(validators=[InputRequired()], default='users')


class CreateUserForm(UserForm):
    """회원가입 폼"""

    password = PasswordField(label='비밀번호', validators=[InputRequired()])

    def validate_name(self, extra):
        try:
            session.query(User) \
                   .filter_by(name=self.name.data) \
                   .one()
        except NoResultFound:
            pass
        else:
            raise ValidationError('User(name={}) already exists'
                                  .format(self.name.data))
