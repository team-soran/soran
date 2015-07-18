from soran import Album
from soran.archive import Archive
from soran.service import NAVER
from soran.web.forms.archive import ArchiveForm, CreateAlbumForm

from .util import MultiDict


def test_create_album_form():
    album = Album()
    album_name = u'My favourite faded fantasy'
    album_service_id = u'a123'
    form = CreateAlbumForm(formdata=MultiDict([
        ('name', album_name),
        ('service_id', album_service_id),
    ]))
    assert form.validate()
    form.populate_obj(album)
    assert album.name == album_name
    assert album.service_id == album_service_id

