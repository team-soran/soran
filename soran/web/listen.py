""":mod:`soran.web.listen` --- log listend song
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import request

from ..datetime import now
from ..validate import Argument, DatetimeArgument, Validator, required
from .response import bad_syntax, ok
from .route import APIBlueprint


listen = APIBlueprint('listen', __name__, template_folder='templates/listen',
                      url_prefix='/listen')


class ListenNaverValidator(Validator):
    """Validator for :func:`listen_naver` . """

    listend_at = DatetimeArgument(default=now())

    name = Argument(validators=[required])

    artist_name = Argument(validators=[required])

    album_name = Argument(validators=[required])


@listen.route('/naver/', methods=['POST'])
def listen_naver(song_id):
    """Archive listen log.

    :param song_id:
    :return:
    """
    args = ListenNaverValidator(request.args)
    if not args.validate():
        return bad_syntax()
    return ok()
