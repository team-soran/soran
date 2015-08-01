""":mod:`soran.web.listen` --- log listend song
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint, Response, request

from ...archive import Archive
from ...db import session
from ...forms.archive import ArchiveNaverForm
from ..helper import ensure_transaction
from ..response import APIBadRequest, json_result


listen = Blueprint('listen', __name__, url_prefix='/listen')


@listen.route('/naver/', methods=['POST'])
def listen_naver() -> Response:
    """Archive listen log.

    :return:

    """
    args = ArchiveNaverForm(formdata=request.form)
    if not args.validate():
        raise APIBadRequest(description=args.erros)
    archive = Archive()
    args.populate_obj(archive)
    with ensure_transaction(session):
        session.add(archive)
    return json_result(status=200)
