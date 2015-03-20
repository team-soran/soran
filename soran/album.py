from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

from .db import Base
from .mixin import BaseMixin
from .artist import Artist
from .song import Song


class AlbumArtistAssoc(Base):
    __tablename__ = 'album_artist_assoc'

    id = Column(Integer, primary_key=True)

    album_id = Column(Integer, ForeignKey('albums.id'))

    artist_id = Column(Integer, ForeignKey('artists.id'))

    album = relationship('Album')

    artists = relationship('Artist')


class Album(Base, BaseMixin):
    """Soran album model.
    """
    __tablename__ = 'albums'
    __repr_attr__ = 'name'

    artists = relationship(Artist, secondary='album_artist_assoc')

    songs = relationship(Song)