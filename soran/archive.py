from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer

from .db import Base


class Archive(Base):
    __tablename__ = 'archives'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)

    listened_at = Column(DateTime, nullable=False, default=datetime.now())

    user = relationship('User')

    song = relationship('Song')
