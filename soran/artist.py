from .db import Base
from .mixin import BaseMixin


class Artist(Base, BaseMixin):
    """
    """
    __tablename__ = 'artists'

    __repr_attr__ = 'name'