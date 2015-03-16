from urllib.request import urlopen

import html5lib


__all__ = 'Youtube',


class Youtube:
    _url = 'https://www.youtube.com/watch?v='

    def __init__(self, id_):
        self.id_ = id_
        self.metadata = {}

    def request_metdata(self):
        response = urlopen(self.to_url)
        if response.status != 200:
            raise Exception('status_code: {}, url: {}'.format(
                response.status, self.to_url))
        html = html5lib.parse(response.readall())

    @property
    def to_url(self):
        return _url + self.id_
