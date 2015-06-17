""":mod:`soran.mixin` --- mixins for models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime

from sqlalchemy.orm import validates
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Integer, Unicode

from .service import BUGS, NAVER, SORAN, YOUTUBE


__all__ = 'BaseMixin', 'ServiceMixin', 'NameMixin',


class BaseMixin(object):
    """pk가 필요한 모든 모델이 상속받는 믹스인"""

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


class ServiceMixin(object):
    """소란에서 이용가능한 서비스들의 집합 """

    default_services = set([NAVER, BUGS, YOUTUBE, SORAN])

    service = Column(Unicode, nullable=False)

    service_id = Column(Unicode, nullable=True)

    @validates('service')
    def validate_service(self, key, service):
        assert service in self.default_services
        return service


class NameMixin(BaseMixin):

    name = Column(Unicode, nullable=False)

    __repr_attr__ = 'id', 'name',
