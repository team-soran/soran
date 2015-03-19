from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table

from .db import Base
from .mixin import BaseMixin
from .artist import Artist
from .song import Song

artist_association_table = Table('posts_artist_assoc', Base.metadata,
                          Column('album_id', Integer, ForeignKey('albums.id')),
                          Column('artist_id', Integer, ForeignKey('artists.id')))


class Album(Base, BaseMixin):
    """Soran album model.
    """
    __tablename__ = 'albums'

    __repr_attr__ = 'name'

    artist = relationship(Artist, secondary=artist_association_table)
    song = relationship(Song)