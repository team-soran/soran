""":mod:`soran.album` --- soran album
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer

from .db import Base
from .mixin import BaseMixin, NameMixin, ServiceMixin


__all__ = 'AlbumArtistAssoc', 'Album',


class AlbumArtistAssoc(Base, BaseMixin):

    album_id = Column(Integer, ForeignKey('albums.id'))

    artist_id = Column(Integer, ForeignKey('artists.id'))

    album = relationship('Album')

    artists = relationship('Artist')

    __tablename__ = 'album_artist_assoc'


class Album(Base, NameMixin, ServiceMixin):
    """Soran album model.
    """

    __tablename__ = 'albums'

    artists = relationship('Artist', secondary='album_artist_assoc')

    songs = relationship('Song')
