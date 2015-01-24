from flask import current_app, g
from werkzeug.local import LocalProxy
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__all__ = ('Base', 'ensure_shutdown_session', 'get_engine', 'get_session',
           'session', 'Session')

def ensure_shutdown_session(app):
    """:py:attr:`dam.web.app.app` 의 문맥이 종료될때,
    :py:attr:`dam.db.session` 이 반드시 닫히도록 합니다.

    :param flask.Flask app: dam의 flask 앱 :py:mod:`dam.web.app` .
    """
    def close_session(exc=None):
        if hasattr(g, 'sess'):
            if exc:
                g.sess.rollback()
            g.sess.close()

    app.teardown_appcontext(close_session)


def get_engine():
    """DB 연결에 필요한 엔진을 생성합니다.

    :return: :py:mod:`sqlalchemy` 의 엔진
    :rtype: :py:class:`sqlalchemy.engine.Engine`
    """
    config = current_app.config
    if 'DATABASE_ENGINE' in config:
        return config['DATABASE_ENGINE']
    config['DATABASE_ENGINE'] = create_engine(config['DATABASE_URL'])
    return config['DATABASE_ENGINE']


def get_alembic_config(engine):
    """:py:mod:`alembic` 에필요한 설정을 가져옵니다.

    :param engine: db에 연결할 :py:class:`sqlalchemy.engine.Engine` 인스턴스
    :return: alembic 사용할때 필요한 설정이 담긴
             :py:class:`alembic.config.Config`
    :rtype: :py:class:`alembic.config.Config`
    """
    if not isinstance(engine, Engine):
        raise Exception('boilerplate.db.get_alembic_config: engine is not'
                        '`Engine`')
    config = Config()
    config.set_main_option('script_location', 'boilerplate:migrations')
    config.set_main_option('sqlalchemy.url', str(engine.url))
    return config


def get_session(engine=None):
    """:py:mod:`sqlalchemy` 의 쿼리를 날릴때 사용하는 세션을 가지고옵니다.

    :param sqlalchemy.engine.Engine engine: :py:mod:`sqlalchemy` 엔진
    :return: DB에 쿼리를 날리때 사용하는 세션
    :rtype: :py:class:`sqlalchemy.orm.session.Session`
    """
    if engine is None:
        engine = get_engine()
    if hasattr(g, 'sess'):
        return g.sess
    session = Session(bind=engine)
    try:
        g.sess = session
    except RuntimeError:
        pass
    return session


Base = declarative_base()
Session = sessionmaker()
session = LocalProxy(get_session)
