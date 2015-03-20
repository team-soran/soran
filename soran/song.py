from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

from .db import Base
from .mixin import BaseMixin


class Song(Base, BaseMixin):
    """Soran song model.
    """
    __tablename__ = 'songs'
    __repr_attr__ = 'name'

    album_id = Column(Integer, ForeignKey('albums.id'))

    album = relationship('Album')