""":mod:`soran.web.listen` --- log listend song
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import request

from .forms.archive import ListenNaverForm
from .response import bad_syntax, ok
from .route import APIBlueprint


listen = APIBlueprint('listen', __name__, template_folder='templates/listen',
                      url_prefix='/listen')


@listen.route('/naver/', methods=['POST'])
def listen_naver(song_id):
    """Archive listen log.

    :param song_id:
    :return:
    """
    args = ListenNaverForm(request.args)
    if not args.validate():
        return bad_syntax()
    return ok()
