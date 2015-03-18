""":mod:`soran.web.user` --- soran secret youtube API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint, jsonify

from .response import ok
from ..db import session


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
        abort(500)
    return ''
