from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime

from .db import Base


class Archive(Base):
    __tablename__ = 'archives'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)

    listened_at = Column(DateTime, nullable=False)

    users = relationship('User')

    songs = relationship('Song')