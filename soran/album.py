from .db import Base
from .mixin import BaseMixin


class Album(Base, BaseMixin):
    """
    """
    __tablename__ = 'albums'

    __repr_attr__ = 'name'