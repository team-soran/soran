from flask import json
from pytest import mark

from soran.user import User
from soran.web.app import app
from soran.web.auth import soran_token

from .util import url_for

def test_web_create_user(f_session):
    username = 'aaa'
    password = 'abc'
    service = 'naver'
    data = {'username': username, 'password': password, 'service': service}
    with app.test_client() as client:
        response = client.post(url_for('user.create'), data=data)
    assert 201 == response.status_code
    assert response.data
    response_data = json.loads(response.data)
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


@mark.parametrize('emit', ('service', 'password', 'username'))
def test_web_badsyntax_create_user(f_session, emit):
    username = 'aaa'
    password = 'abc'
    service = 'naver'
    data = {'username': username, 'password': password, 'service': service}
    del data[emit]
    with app.test_client() as client:
        response = client.post(url_for('user.create'), data=data)
    assert 400 == response.status_code


@mark.parametrize('emit', ('password', 'username'))
def test_web_badsyntax_authorize_user(f_session, emit):
    username = 'aaa'
    password = 'abc'
    data = {'username': username, 'password': password}
    del data[emit]
    with app.test_client() as client:
        response = client.post(url_for('user.authorize'), data=data)
    assert 400 == response.status_code


def test_web_authorize_user(f_session, f_user):
    data = {'username': f_user.username, 'password': f_user.password}
    with app.test_client() as client:
        response = client.post(url_for('user.authorize'), data=data)
    assert 200 == response.status_code
    assert response.data
    response_data = json.loads(response.data)
    assert 'data' in response_data
    assert 'token' in response_data['data']
    assert response_data['data']['token']
    expected_token = soran_token(f_user)
    assert expected_token == response_data['data']['token']


@mark.parametrize('weird', ('password', 'username'))
def test_web_notfound_authroize_user(f_session, f_user, weird):
    data = {'username': f_user.username, 'password': f_user.password}
    data[weird] += 'werid-sentence'
    with app.test_client() as client:
        response = client.post(url_for('user.authorize'), data=data)
    assert 404 == response.status_code
