from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode, DateTime


class BaseMixin:
    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    service = Column(Unicode, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)

    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    __repr_attr__ = 'id'

    def __repr__(self):
        represents = []
        for attr in self.__repr_attr__:
            represents.append('{}={}'.format(attr, getattr(self, attr)))
        return '{0.__class__.__name__}({1}) @ {2}'.format(
            self, ', '.join(represents), hex(id(self)))