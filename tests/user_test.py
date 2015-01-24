from soran.user import User

def test_create_user(f_session):
    username = 'aaa'
    password = 'abc'
    service = 'naver'
    user = User(username=username, password=password, service=service)
    f_session.add(user)
    f_session.commit()
    find_user = f_session.query(User)\
                .filter(User.username == username)\
                .first()
    assert find_user
    assert hasattr(find_user, 'id')
    assert find_user.id
    assert hasattr(find_user, 'created_at')
    assert find_user.created_at
    assert hasattr(find_user, 'modified_at')
    assert find_user.modified_at
    assert username == find_user.username
    assert password == find_user.password
    assert service == find_user.service
