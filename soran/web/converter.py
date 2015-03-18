from werkzeug.routing import BaseConverter
from ..ytb import Youtube


__all__ = 'YoutubeConverter',


class YoutubeConverter(BaseConverter):
    def to_python(self, value):
        return Youtube(value)

    def to_url(self, value):
        return value.to_url()
