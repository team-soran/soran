from sqlalchemy.orm import relationship

from .db import Base
from .mixin import BaseMixin
from .artist import Artist
from .song import Song


class Album(Base, BaseMixin):
    """Soran album model.
    """
    __tablename__ = 'albums'

    __repr_attr__ = 'name'

    artist_id = relationship(Artist)
    song_id = relationship(Song)