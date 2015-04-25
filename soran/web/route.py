""":mod:`soran.web.route` --- soran route helper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint


__all__ = 'APIBlueprint', 'API_PREFIX', 'API_ENDPOINT_POSTFIX', 'API_ENDPOINT',


API_PREFIX = 'api'
API_ENDPOINT_POSTFIX = '@'
API_ENDPOINT = '{prefix}{postfix}'.format(prefix=API_PREFIX,
                                          postfix=API_ENDPOINT_POSTFIX)


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
                                  '{0}{1}{2}'.format(api_prefix,
                                                     API_ENDPOINT_POSTFIX,
                                                     endpoint),
                                  f, **options)
            return f

        return decorator
