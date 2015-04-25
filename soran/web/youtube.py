""":mod:`soran.web.user` --- soran secret youtube API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint
from werkzeug.exceptions import InternalServerError

from .response import ok


bp = Blueprint('youtube', __name__, template_folder='templates/youtube')


@bp.route('/<youtube:youtube>/', methods=['GET'])
def find(youtube):
    """Find meta data for given youtube.
    """
    try:
        youtube.request_metdata()
    except Exception as e:
        return ok(message=e.message)
    if not youtube.metadata:
        raise InternalServerError()
    return ''
