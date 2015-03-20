from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

from .db import Base
from .user import Person
from .song import Song


class ArtistSongAssoc(Base):
    __tablename__ = 'artist_song_assoc'

    id = Column(Integer, primary_key=True)

    artist_id = Column(Integer, ForeignKey('artists.id'))

    song_id = Column(Integer, ForeignKey('songs.id'))

    artists = relationship('Artist')

    songs = relationship('Song')


class Artist(Person):
    """Soran artist model.
    """
    __tablename__ = 'artists'
    __repr_attr__ = 'name'
    __mapper_args__ = {'polymorphic_identity': 'artists'}

    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)

    songs = relationship(Song, secondary='artist_song_assoc')