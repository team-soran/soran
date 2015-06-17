""":mod:`soran.web.forms.listen` --- :mod:`~soran.web.listen` 에 관계 있는 폼
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from . import BaseForm, BaseFormField, FixedValueField, ServiceForm
from ...service import NAVER


__all__ = (
    'ArchiveForm', 'ArchiveNaverForm',
    'CreateAlbumForm', 'CreateArtistForm', 'CreateSongForm',
)


class CreateAlbumForm(BaseForm):
    """앨범 양식"""

    pass


class CreateArtistForm(BaseForm):
    """가수 양식"""

    pass


class CreateSongForm(BaseForm):
    """노래 양식"""

    pass


class ArchiveForm(ServiceForm):
    """노래 청취 기록 양식"""

    album = BaseFormField(CreateAlbumForm, label=u'음악')


class ArchiveNaverForm(ArchiveForm):
    """네이버 뮤직 음악 청취 기록 양식"""

    service = FixedValueField(value=NAVER)
