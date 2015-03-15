from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime

from .db import Base


class Music(Base):
    """ Soran music model.
    """
    __tablename__ = 'Music'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    album = Column(Unicode, nullable=False)

    artist = Column(Unicode, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)

    modified_at = Column(DateTime, nullable=False, default=datetime.now)

    count = Column(Integer, nullable=False, default=0)

    service = Column(Unicode, nullable=False)

    username = Column(Integer, ForeignKey('persons.id'), primary_key=True)

    __mapper_args__ = {'polymorphic_on': service}


class Naver(Music):
    """ NaverMusic Model, This model is inherited by Music model.
    """
    __mapper_args__ = {'polymorphic_identity': 'naver'}
    __tablename__ = 'naver'

    id = Column(Integer, ForeignKey('Music.id'), primary_key=True)

    service_id = Column(Integer, nullable=False)


class Bugs(Music):
    """ Bugs Model, This model is inherited by Music model.
    """
    __mapper_args__ = {'polymorphic_identity': 'bugs'}
    __tablename__ = 'bugs'

    id = Column(Integer, ForeignKey('Music.id'), primary_key=True)

    service_id = Column(Integer, nullable=False)