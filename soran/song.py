from .db import Base
from .mixin import BaseMixin


class Song(Base, BaseMixin):
    """
    """
    __tablename__ = 'songs'

    __repr_attr__ = 'name'
