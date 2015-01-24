from flask import url_for as flask_url_for

from soran.web.app import app

def url_for(*args, **kwargs):
    with app.test_request_context() as ctx_:
        return flask_url_for(*args, **kwargs)
