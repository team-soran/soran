""":mod:`soran.web.route` --- soran route helper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint, Response as FlaskResponse, request


__all__ = 'APIBlueprint', 'API_PREFIX',


API_PREFIX = 'api'


class APIBlueprint(Blueprint):
    """Routing api automatically
    """

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop("endpoint", f.__name__)
            api = options.pop('api', False)
            self.add_url_rule(rule, endpoint, f, **options)
            api_prefix = API_PREFIX
            if api:
                self.add_url_rule('/{}{}'.format(api_prefix, rule),
                                  '{}@{}'.format(api_prefix, endpoint),
                                  f, **options)
            return f

        return decorator
