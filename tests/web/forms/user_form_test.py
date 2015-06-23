from soran.user import User
from soran.web.forms.user import CreateUserForm

from .._helper import formify


def test_form_create_user(f_app, f_session):
    with f_app.test_request_context():
        user = User()
        username = 'myusername'
        payload = formify({
            'who': 'users',
            'service': 'naver',
            'name': username,
            'password': 'oiefw'
        })
        a = CreateUserForm(payload)
        a.populate_obj(obj=user)
        print(user)
        print(user.name)
        f_session.add(user)
        f_session.commit()
        find_user = f_session.query(User) \
                             .filter(User.name == username) \
                             .first()
        assert find_user
