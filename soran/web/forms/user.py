""":mod:`soran.web.forms.user` --- 사용자와 관계있는 폼들
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from wtforms import HiddenField, PasswordField, StringField
from wtforms.validators import InputRequired

from . import ServiceForm


__all__ = 'CreateUserForm', 'UserForm',


class UserForm(ServiceForm):
    """사용자 폼"""

    name = StringField(label='이름', validators=[InputRequired()])

    who = HiddenField(validators=[InputRequired()], default='users')


class CreateUserForm(UserForm):
    """회원가입 폼"""

    password = PasswordField(label='비밀번호', validators=[InputRequired()])
