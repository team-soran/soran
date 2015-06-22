from pytest import fixture

from soran.user import User


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


@fixture
def f_user():
    name = 'aaa'
    password = 'abc'
    service = 'naver'
    return User(name=name, password=password, service=service)