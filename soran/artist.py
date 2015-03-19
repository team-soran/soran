from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table

from .db import Base
from .user import Person
from .song import Song

song_association_table = Table('posts_song_assoc', Base.metadata,
                          Column('artist_id', Integer, ForeignKey('artists.id')),
                          Column('song_id', Integer, ForeignKey('songs.id')))


class Artist(Person):
    """Soran artist model.
    """
    __tablename__ = 'artists'
    __repr_attr__ = 'name'
    __mapper_args__ = {'polymorphic_identity': 'users'}

    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    song = relationship(Song, secondary=song_association_table)