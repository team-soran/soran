""":mod:`soran.validate` --- request arguments validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import datetime as py_datetime
from functools import partial

from annotation.typed import optional

from . import datetime


__all__ = ('FloatArgument', 'Argument', 'Validator', 'TypeArgument',
           'IntArgument', 'is_datetime', 'is_float', 'is_int', 'is_this_type',
           'required')


def is_this_type(type_: type, data) -> bool:
    """Check data can be converted to specific types.

    :param type_:
    :type type_: :class:`type`
    :param data: a request data to be checked.
    :return: whether data can be converted to ``type`` .
    :rtype: bool
    """
    result = True
    if data is None:
        return result
    try:
        type_(data)
    except ValueError:
        result = False
    return result


def is_int(data) -> bool:
    """Check data can be converted to integer.

    :param data: a request data to be checked.
    :return: whether data can be integer.
    :rtype: bool
    """
    return is_this_type(int, data)


def is_float(data) -> bool:
    """Check data can be converted to float.

    :param data: a request data to be checked.
    :return: whether data can be converted to float.
    :rtype: bool
    """
    return is_this_type(float, data)


def required(data) -> bool:
    """Check data is provided.

    :param data: a request data to be checked.
    :return: whether data is supplied or not.
    :rtype: bool
    """
    return bool(data)


def is_datetime(data) -> bool:
    result = True
    try:
        datetime.parse(data)
    except Exception:
        result = False
    return result


class Argument:
    """Represent payload's argument.

    it is similar to ``Field`` in wtforms.

    :param list validators: a list of validator.
    :param name: argument's name if it is ``None`` ,
                 use variable name in :class:`Validator` .
    :param default: a default value when data is ``None`` .
    """

    def __init__(self, validators: list, name=None, default=None):
        self.validators = validators
        self.name = name
        self._data = None
        self.errors = []
        if default is not None:
            for validator in self.validators:
                assert validator(default), '{}'.format(validator.__name__)
        self.default = default

    @property
    def d(self):
        return self._data

    @d.setter
    def d(self, value):
        if value is None and self.default is not None:
            self._data = self.default
        else:
            self._data = value

    def validate(self, data) -> bool:
        result = True
        for valid_func in self.validators:
            if not valid_func(data):
                result = False
                if not hasattr(valid_func, '__name__'):
                    setattr(valid_func, '__name__', repr(valid_func))
                self.errors.append(valid_func.__name__)
        return result

    def convert(self, data):
        return data

    def populate(self, data):
        self.d = self.convert(data)


class TypeArgument(Argument):
    """Argument which check its types.

    :param type type_:
    :param list validators: a list of validator.
    :param name: argument's name if it is ``None`` ,
                 use variable name in :class:`Validator` .
    :param default: a default value when data is ``None`` .
    """

    def __init__(self, type_: type, validators: list, name: str=None,
                 default=None):
        self.type_ = type_
        super(TypeArgument, self).__init__(validators=validators, name=name,
                                           default=default)
        self.validators.append(partial(is_this_type, type_))

    def convert(self, data):
        if data is None:
            return data
        return self.type_(data)


class IntArgument(TypeArgument):
    """Assure type of argument is int.

    :param list validators: a list of validator.
    :param str name: argument's name if it is ``None`` ,
                     use variable name in :class:`Validator` .
    :param int default: a default value when data is ``None`` .
    """

    def __init__(self, validators: list=[], name: str=None,
                 default: int=None):
        super(IntArgument, self).__init__(int, validators=validators,
                                          name=name, default=default)


class FloatArgument(TypeArgument):
    """Assure type of argument is float.

    :param list validators: a list of validator.
    :param str name: argument's name if it is ``None`` ,
                     use variable name in :class:`Validator` .
    :param float default: a default value when data is ``None`` .
    """

    def __init__(self, validators: list=[], name: str=None,
                 default: float=None):
        super(FloatArgument, self).__init__(float, validators=validators,
                                            name=name, default=default)


class DatetimeArgument(Argument):

    def __init__(self, validators: list=[], default: optional(datetime)=None,
                 name: optional(str)=None):
        validators.append(is_datetime)
        super(DatetimeArgument, self).__init__(validators=validators,
                                               name=name,
                                               default=default)

    def convert(self, data):
        if not (isinstance(data, py_datetime.datetime) or
                isinstance(data, py_datetime.date)):
            return datetime.parse(data)
        return data


class Validator:
    """Validate payload.

    it provide feature like wtforms, but can apply to every payload.
    each validator implemented by inherit this class.

    .. sourcecode:: python

       class MyCustomValidator(Validator):

           some_name = Argument(validators=[required])

           ...

       @app.route(...)
       def some_route():
           arg = MyCustomValidator(request.args)
           if arg.validate():
               ...

    :param dict payload: payload to be validated.
    """

    def __init__(self, payload: dict={}):
        self.payload = payload
        self.errors = []

    def validate(self) -> bool:
        """Validate arguments.

        :return: whether given arguments are validate or not.
        :rtype: bool
        """
        result = True
        for argument in self.arguments:
            data = self.payload.get(argument.name, argument.default)
            if not argument.validate(data):
                result = False
                self.errors.append({argument.name: argument.errors})

        return result

    def populate(self):
        """Populate data to its argument to use :attr:`Argument.d`."""
        for argument in self.arguments:
            argument.populate(self.payload.get(argument.name))

    @property
    def arguments(self):
        """Get all arguments in validator."""
        for arg_name in dir(self):
            argument = getattr(self, arg_name)
            if isinstance(argument, Argument):
                if not argument.name:
                    argument.name = arg_name
                yield argument
