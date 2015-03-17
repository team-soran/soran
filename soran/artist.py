from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table

from .db import Base
from .mixin import BaseMixin
from .song import Song

association_table = Table('association', Base.metadata,
                          Column('artist_id', Integer, ForeignKey('artists.id')),
                          Column('song_id', Integer, ForeignKey('songs.id')))


class Artist(Base, BaseMixin):
    """Soran artist model.
    """
    __tablename__ = 'artists'

    __repr_attr__ = 'name'

    album_id = Column(Integer, ForeignKey('albums.id'))
    song = relationship(Song, secondary=association_table)