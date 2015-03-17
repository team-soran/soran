from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode, DateTime

from .db import Base


class Album(Base):
    """
    """
    __tablename__ = 'albums'

    __repr_attr__ = 'name'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    service = Column(Unicode, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)

    updated_at = Column(DateTime, nullable=False, default=datetime.now)