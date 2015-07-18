from flask import url_for as flask_url_for

from soran import app


def url_for(*args, **kwargs):
    with app.test_request_context():
        return flask_url_for(*args, **kwargs)
