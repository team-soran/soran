from annotation.typed import typechecked
from werkzeug.datastructures import MultiDict as WerkzeugMultiDict

from soran.app import app


@typechecked
def MultiDict(l: list) -> WerkzeugMultiDict:
    with app.test_request_context():
        return WerkzeugMultiDict(l)