""":mod:`soran.archive` --- 청취한 음악들을 기록하고 저장합니다.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer

from .db import Base


__all__ = 'Archive',


class Archive(Base):
    """청취한 내용을 기록합니다"""

    __tablename__ = 'archives'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)

    listened_at = Column(DateTime, nullable=False, default=datetime.now())

    user = relationship('User')

    song = relationship('Song')

    @property
    def song_(self):
        """:meth:`wtforms.Form.populate_obj` 를 지원하기위한 속성"""
        pass

    @song_.setter
    def song_(self, song):
        """:meth:`wtforms.Form.populate_obj` 를 지원하기위한 속성"""
        pass

    @property
    def album(self):
        """:meth:`wtforms.Form.populate_obj` 를 지원하기위한 속성"""
        return self.song.album

    @album.setter
    def album(self, album):
        """:meth:`wtforms.Form.populate_obj` 를 지원하기위한 속성"""
        pass

    @property
    def artist(self):
        """:meth:`wtforms.Form.populate_obj` 를 지원하기위한 속성"""
        return self.song.album

    @album.setter
    def artist(self, album):
        """:meth:`wtforms.Form.populate_obj` 를 지원하기위한 속성"""
        pass
