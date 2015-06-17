from werkzeug.datastructures import MultiDict as WerkzeugMultiDict

from soran.web.app import app


def MultiDict(l):
    with app.test_request_context():
        return WerkzeugMultiDict(l)