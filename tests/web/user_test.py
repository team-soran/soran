from urllib.parse import urlparse

from flask import json
from pytest import mark

from soran.user import User
from soran.web.auth import Token
from soran.web.user import CreateUserForm

from werkzeug.datastructures import MultiDict

from .util import url_for


def test_web_create_user(f_app):
    username = 'aaa'
    password = 'abc'
    service = 'naver'
    who = 'users'
    data = {'name': username, 'password': password, 'service': service,
            'who': who}
    with f_app.test_client() as client:
        response = client.post(url_for('user.create'), data=data)
    assert 302 == response.status_code
    url = urlparse(response.headers.get('Location'))
    assert url.path == url_for('hello')


@mark.parametrize('emit', ('service', 'password', 'username'))
def test_web_badsyntax_create_user(f_app, emit):
    username = 'aaa'
    password = 'abc'
    service = 'naver'
    data = {'username': username, 'password': password, 'service': service}
    del data[emit]
    with f_app.test_client() as client:
        response = client.post(url_for('user.create'), data=data)
    assert 400 == response.status_code


@mark.parametrize('emit', ('password', 'username'))
def test_web_badsyntax_authorize_user(f_session, emit, f_app):
    username = 'aaa'
    password = 'abc'
    data = {'username': username, 'password': password}
    del data[emit]
    with f_app.test_client() as client:
        response = client.post(url_for('user.authorize'), data=data)
    assert 400 == response.status_code


def test_web_authorize_user(f_app, f_user):
    data = {'username': f_user.name, 'password': 'password:hello'}
    with f_app.test_client() as client:
        response = client.post(url_for('user.authorize'), data=data)
    assert 302 == response.status_code
    url = urlparse(response.headers.get('Location'))
    assert url.path == url_for('hello')


def test_web_api_authorize_user(f_app, f_user):
    data = {'username': f_user.name, 'password': 'password:hello'}
    with f_app.test_client() as client:
        response = client.post(url_for('user.api@authorize'), data=data)
    assert 201 == response.status_code
    assert response.data
    response_data = json.loads(response.data)
    assert 'data' in response_data
    assert 'token' in response_data['data']
    assert response_data['data']['token']
    expected_token = Token(user=f_user)
    assert expected_token.token == response_data['data']['token']


@mark.parametrize('weird', ('password', 'username'))
def test_web_notfound_authroize_user(f_session, f_user, weird, f_app):
    data = {'username': f_user.name, 'password': f_user.password}
    data[weird] = 'werid-sentence'
    with f_app.test_client() as client:
        response = client.post(url_for('user.authorize'), data=data)
    assert 404 == response.status_code


def test_web_api_create_user(f_session, f_app):
    username = 'aaa'
    password = 'abc'
    service = 'naver'
    who = 'users'
    data = {'name': username, 'password': password, 'service': service,
            'who': who}
    with f_app.test_client() as client:
        response = client.post(url_for('user.api@create'), data=data)
    assert 201 == response.status_code
    response_data = json.loads(response.data)
    assert response_data
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


def test_web_sign_up_form(f_app):
    with f_app.test_request_context():
        user = User()
        username = 'seotaiji'
        password = 'abc'
        service = 'naver'
        who = 'users'
        form = CreateUserForm(formdata=MultiDict([
            ('name', username),
            ('password', password),
            ('service', service),
            ('who', who),
        ]))
        assert form.validate()
        form.populate_obj(user)
        assert user.name == username
        assert user.password == password
        assert user.service == service
        assert user.who == who
