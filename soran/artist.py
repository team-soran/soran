""":mod:`soran.artist` --- soran artist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer

from .db import Base
from .mixin import BaseMixin
from .user import Person


__all__ = 'ArtistSongAssoc', 'Artist',


class ArtistSongAssoc(Base, BaseMixin):
    """Association between :class:`Artist` and :class:`Song` .
    """

    artist_id = Column(Integer, ForeignKey('artists.id'))

    song_id = Column(Integer, ForeignKey('songs.id'))

    artists = relationship('Artist')

    songs = relationship('Song')

    __tablename__ = 'artist_song_assoc'


class Artist(Person):
    """Soran artist model.
    """

    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)

    songs = relationship('Song', secondary='artist_song_assoc')

    __tablename__ = 'artists'

    __mapper_args__ = {'polymorphic_identity': 'artists'}
