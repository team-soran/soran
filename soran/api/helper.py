import contextlib

from sqlalchemy.exc import IntegrityError

from .response import APIIntegrityError


__all__ = 'ensure_transaction',


@contextlib.contextmanager
def ensure_transaction(sess):
    try:
        yield
        sess.commit()
    except IntegrityError as e:
        sess.rollback()
        raise APIIntegrityError(description=e)
