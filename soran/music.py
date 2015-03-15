from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime

from .db import Base


class Music(Base):
    """ Soran music model.
    """
    __tablename__ = 'Music'

    id = Column(Integer, primary_key=True)

    title = Column(Unicode, nullable=False)

    album = Column(Unicode, nullable=False)

    artist = Column(Unicode, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)

    modified_at = Column(DateTime, nullable=False, default=datetime.now)

    count = Column(Integer, nullable=False, default=0)

    type = Column(Unicode, nullable=False)

    user = Column(Integer, ForeignKey('persons.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'music',
        'polymorphic_on': type
    }


class NaverMusic(Music):
    """ NaverMusic Model, This model is inherited by Music model.
    """
    __tablename__ = 'NaverMusic'

    id = Column(Integer, ForeignKey('Music.id'), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': 'naver_music'}


class Bugs(Music):
    """ Bugs Model, This model is inherited by Music model.
    """
    __tablename__ = 'bugs'

    id = Column(Integer, ForeignKey('Music.id'), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': 'bugs'}