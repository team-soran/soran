#!/usr/bin/env python
from collections import namedtuple
import os
import logging.config


from alembic.command import (
    branches as alembic_branch,
    current as alembic_current,
    downgrade as alembic_downgrade,
    history as alembic_history,
    revision as alembic_revision,
    upgrade as alembic_upgrade
)
from alembic.script import ScriptDirectory
import click

from soran.app import app
from soran.config import read_config
from soran.db import get_alembic_config, get_engine, session


class _Config(object):

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


    def __init__(self, path):
        self.abspath = os.path.abspath(path)
        self.configuration = read_config(self.abspath)

    @property
    def alembic_config(self):
        alembic_config = get_alembic_config(
            get_engine(self.configuration)
        )
        logging.config.dictConfig(self.ALEMBIC_LOGGING)
        return alembic_config


pass_config = click.make_pass_decorator(_Config)


@click.group()
@click.option('--config', '-c', help='configuration', required=True)
@click.pass_context
def cli(ctx, config):
    ctx.obj = _Config(path=config)


@cli.command()
@click.option('--host', default='127.0.0.1',
              help=('the hostname to listen on. Set this to `0.0.0.0` to'
                    'have the server available externally as well. Defaults to'
                    '`127.0.0.1`.'))
@click.option('--port', default=5000, type=int,
              help=('the port of the webserver. Defaults to `5000` or the'
                    'port defined in the `SERVER_NAME` config variable if'
                    'present.'))
@click.option('--debug/--no-debug', 'use_debugger', is_flag=True, default=True,
              help='if given, enable or disable debug mode.')
@click.option('--reload/--no-reload', 'use_reloader', is_flag=True,
              default=True,
              help=('hould the server automatically restart'
                    'the python process if modules were changed?'))
@click.option('--threaded', is_flag=True,
              help=('should the process handle each request in'
                    'a separate thread?'))
@click.option('--processes', default=1, type=int,
              help=('if greater than 1 then handle each request in a new'
                    'process up to this maximum number of concurrent'
                    'processes.'))
@click.option('--passthrough-errors', is_flag=True,
              help=('set this to True to disable the error catching.'
                    'This means that the server will die on errors but it'
                    'can be useful to hook debuggers in (pdb etc.)'))
@pass_config
def serve(
        _config, host, port, use_debugger, use_reloader, threaded, processes,
        passthrough_errors):
    """Serve a there flask app.
    """
    try:
        app.config.update(_config.configuration)
    except Exception as e:
        raise click.UsageError(str(e))
    else:
        app.run(host=host,
                port=port,
                debug=use_debugger,
                use_debugger=use_debugger,
                use_reloader=use_reloader,
                threaded=threaded,
                processes=processes,
                passthrough_errors=passthrough_errors)


class RelativeRevisionParamType(click.ParamType):

    _RelativeRivision = namedtuple('_RelativeRevision', ['upgrade', 'n'])

    name = 'alembic_relative_revision'

    def convert(self, value, param, ctx):
        try:
            _c = int(value)
        except ValueError:
            raise click.BadParameter(message=value,
                                     param_hint=self.__class__.__name__)
        else:
            return self._RelativeRivision(upgrade=_c > 0, n=value)

    def __repr__(self):
        return self.name


@cli.command()
@click.argument('revision', required=False)
@click.option('--relative-revision', '-@', type=RelativeRevisionParamType())
@pass_config
def checkout(_config, relative_revision, revision):
    alembic_config = _config.alembic_config
    script = ScriptDirectory.from_config(alembic_config)
    all_revisions = [rev.revision for rev in script.walk_revisions()]
    if revision == 'head':
        alembic_upgrade(alembic_config, revision)
    elif revision is not None:
        if revision not in all_revisions:
            raise click.UsageError('No such a revision: {}, '
                                   'check `history` to find appropriate '
                                   'revision.'.format(revision))
        try:
            alembic_upgrade(alembic_config, revision)
        except Exception:
            alembic_downgrade(alembic_config, revision)
    elif relative_revision and relative_revision.upgrade:
        alembic_upgrade(alembic_config, relative_revision.n)
    elif relative_revision:
        alembic_downgrade(alembic_config, relative_revision.n)
    else:
        raise click.BadParameter(
            'onf of `relatie_revision`, `revision` MUST be required.')


@cli.command()
@click.argument('revision_range', default=None, required=False)
@click.option('--verbose', '-v', default=False, is_flag=True)
@pass_config
def history(_config, revision_range, verbose):
    alembic_config = _config.alembic_config
    alembic_history(alembic_config, revision_range, verbose)


@cli.command()
@click.option('--autogenerate/--no-autogenerate', default=True, is_flag=True)
@click.option('--sql', required=False)
@click.option('--message', '-m', type=click.STRING, required=True)
@click.option('--head', type=click.STRING, default='head')
@click.option('--splice/--no-splice', required=False, default=False,
              is_flag=True)
@click.option('--branch-label', required=False)
@click.option('--version-path', required=False)
@click.option('--rev-id', required=False)
@pass_config
def revision(_config, message, autogenerate, sql, head, splice,
             branch_label, version_path, rev_id):
    alembic_config = _config.alembic_config
    alembic_revision(alembic_config, message, autogenerate, sql, head, splice,
                     branch_label, version_path, rev_id)


@cli.command()
@click.option('--verbose', '-v', default=False, is_flag=True)
@pass_config
def branches(_config, verbose):
    alembic_branch(_config.alembic_config, verbose)


@cli.command()
@click.option('--verbose', '-v', default=False, is_flag=True)
@click.option('--head-only', default=False, is_flag=True)
@pass_config
def current(_config, verbose, head_only):
    alembic_current(_config.alembic_config,verbose, head_only)


if __name__ == '__main__':
    cli()
