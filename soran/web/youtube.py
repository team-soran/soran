""":mod:`soran.web.user` --- soran secret youtube API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint

from .response import bad_syntax, ok


bp = Blueprint('youtube', __name__, template_folder='templates/youtube')


@bp.route('/youtube/<youtube:youtube>/', methods=['GET'])
def find(youtube):
    """Find meta data for given ``youtube`` .
    """
    try:
        youtube.request_metdata()
    except Exception as e:
        return ok(message=e.message)
    if not youtube.metadata:
        return bad_syntax()
    return ''
