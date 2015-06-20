from pytest import fixture

from soran.user import User
from soran.web.user import CreateUserForm

import wtforms


def test_create_user(f_session):
    username = 'aaa'
    password = 'abc'
    service = 'naver'
    user = User(name=username, password=password, service=service)
    f_session.add(user)
    f_session.commit()
    find_user = f_session.query(User)\
                         .filter(User.name == username)\
                         .first()
    assert find_user
    assert hasattr(find_user, 'id')
    assert find_user.id
    assert hasattr(find_user, 'created_at')
    assert find_user.created_at
    assert hasattr(find_user, 'updated_at')
    assert find_user.updated_at
    assert username == find_user.name
    assert password == find_user.password
    assert service == find_user.service


def test_sign_up_form():
    fields = {
        'name': wtforms.StringField,
        'who': wtforms.HiddenField,
        'service': wtforms.HiddenField,
        'password': wtforms.PasswordField,
    }
    for field in fields.items():
        assert isinstance(CreateUserForm, field)


def test_required():
    form = CreateUserForm(name='abc', who='seotaiji', service='naver', password='aaa')
    assert form.validate()


@fixture
def f_user():
    name = 'aaa'
    password = 'abc'
    service = 'naver'
    return User(name=name, password=password, service=service)