""":mod:`soran.song` --- soran song
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

from .db import Base
from .mixin import NameMixin, ServiceMixin


__all__ = 'Song',


class Song(Base, NameMixin, ServiceMixin):
    """Soran song model.
    """

    album_id = Column(Integer, ForeignKey('albums.id'))

    album = relationship('Album')

    __tablename__ = 'songs'
