from urllib.request import urlopen

import html5lib


__all__ = 'Youtube',


class Youtube:
    _url = 'https://www.youtube.com/watch?v='

    def __init__(self, id_):
        self.id_ = id_
        self._metadata = {}

    @property
    def metadata(self):
        if self._metadata:
            return self._metadata
        response = urlopen(self.to_url)
        if response.status != 200:
            raise Exception('status_code: {}, url: {}'.format(
                response.status, self.to_url))
        html = html5lib.parse(response.readall().decode('utf-8'),
                              namespaceHTMLElements=False)
        xpath_builder = "./head//meta[@{attr}='{value}']".format
        query = [
            ('property', 'og:title'),
            ('property', 'og:image'),
            ('name', 'keywords')
        ]
        for attr, value in query:
            elem = html.findall(xpath_builder(attr=attr, value=value))
            if elem:
                self.metadata[value] = elem[0].get('content')
            self._metadata.setdefault(value, None)
        return self._metadata

    @property
    def to_url(self):
        return self._url + self.id_
