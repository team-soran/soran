import logging.config

from alembic.command import (
    branches as alembic_branch,
    current as alembic_current,
    downgrade as alembic_downgrade,
    history as alembic_history,
    revision as alembic_revision,
    upgrade as alembic_upgrade
)
from flask.ext.script import Manager, Shell, prompt_bool

from .config import read_config
from .db import get_alembic_config, get_engine, session
from soran import app


ALEMBIC_LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'generic'
        }
    },
    'formatters': {
        'generic': {
            'format': '%(levelname)-5.5s [%(name)s] %(message)s',
            'datefmt': '%H:%M:%S'
        }
    },
    'root': {
        'level': 'WARN',
        'handlers': ['console']
    },
    'loggers': {
        'alembic': {
            'level': 'INFO',
            'handlers': []
        },
        'sqlalchemy.engine': {
            'level': 'WARN',
            'handlers': []
        }
    }
}


@Manager
def manager(config_path=None):
    config = read_config(config_path)
    app.config.update(config)
    return app


def alembic_config():
    engine = get_engine()
    config = get_alembic_config(engine)
    logging.config.dictConfig(ALEMBIC_LOGGING)
    return config


@manager.option('--revision', '-r', dest='revision', default='head')
def upgrade(revision):
    """리버전의 버전을 올립니다. 특정 리비전이 정해지지않는다면
    가장 최신 리비전으로 버전을 올립니다.
    """
    alembic_upgrade(alembic_config(), revision)


@manager.option('--revision', '-r', dest='revision')
def downgrade(revision):
    """리버전의 버전을 내립니다. 내릴 리비전이 명시적으로 표시되어야합니다.
    """
    alembic_downgrade(alembic_config(), revision)


@manager.command
def history():
    """리비전 기록을 보여줍니다.
    """
    return alembic_history(alembic_config())


@manager.command
def branches():
    """리비전의 브랜치 포인트를 보여줍니다.
    """
    return alembic_branch(alembic_config())


@manager.command
def current():
    """현재 리비전이 어떤 리비전인지 보여줍니다.
    """
    return alembic_current(alembic_config())


@manager.option('--message', '-m', dest='message', default=None)
def revision(message):
    """마이그레이션에 revision을 추가합니다. --autogenerate 물음에 긍정한다면
    자동으로 마이그레이션 스크립트를 생성할 수 있습니다.
    """
    m = "--autogenerate"
    alembic_revision(alembic_config(),
                     message=message,
                     autogenerate=prompt_bool(m, default=True))


def _make_context():
    return dict(app=app, session=session)


manager.add_command("shell", Shell(make_context=_make_context))
manager.add_option('--config', '-c', dest='config_path')

main = manager.run
