""":mod:`soran.web.forms` --- 모든 폼들의 최상위 폼 객체들
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask_wtf import Form
from wtforms import FormField, HiddenField
from wtforms.validators import InputRequired

from ...service import SORAN


__all__ = 'BaseForm', 'BaseFormField',


class BaseForm(Form):
    """최상위 폼 객체

    모든 :class:`wtforms.Form` 에 관계된 객체들은 이 객체를 상속받아 사용합니다.
    """
    pass


class BaseFormField(FormField):
    """최상위 폼필드 객체

    모든 :class:`wtforms.FormField` 에 관계된 객체들은 이 객체를 상속받아 사용합니다.
    """
    pass


class IntegerHiddenField(HiddenField):

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = int(valuelist[0])


class ServiceForm(BaseForm):

    service = HiddenField(validators=[InputRequired()], default=SORAN)


class FixedValueField(HiddenField):

    def widget(self, field, **attrs):
        assert self is field
