""":mod:`soran` --- soran
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode, DateTime

from .db import Base

class User(Base):
    """Soran user model.
    """

    #: name of table.
    __tablename__ = 'users'

    #:
    id = Column(Integer, primary_key=True)

    #:
    username = Column(Unicode, nullable=False)

    #:
    password = Column(Unicode, nullable=False)

    #:
    service = Column(Unicode, nullable=False)

    #:
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    #:
    modified_at = Column(DateTime, nullable=False, default=datetime.now)
