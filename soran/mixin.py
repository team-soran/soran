""":mod:`soran.mixin` --- mixins for models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.orm import validates
from sqlalchemy.types import Integer, Unicode, DateTime


__all__ = 'BaseMixin', 'ServiceMixin', 'NameMixin',


class BaseMixin:

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, nullable=False, default=datetime.now)

    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    __repr_attr__ = 'id',

    def __repr__(self):
        represents = []
        for attr in self.__repr_attr__:
            represents.append('{}={}'.format(attr, getattr(self, attr)))
        return '{0.__class__.__name__}({1}) @ {2}'.format(
            self, ', '.join(represents), hex(id(self)))


class ServiceMixin:

    default_services = set(['naver', 'bugs', 'youtube', 'soran'])

    service = Column(Unicode, nullable=False)

    @validates('service')
    def validate_service(self, key, service):
        assert service in self.default_services
        return service


class NameMixin(BaseMixin):

    name = Column(Unicode, nullable=False)

    __repr_attr__ = 'id', 'name',
