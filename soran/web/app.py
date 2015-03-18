from flask import Flask

from . import user
from .converter import YoutubeConverter

version = 1

app = Flask(__name__)
app.register_blueprint(user.bp, url_prefix='/{}/users'.format(version))


app.url_map.converters.update(
    youtube=YoutubeConverter
)

@app.route('/', methods=['GET'])
def hello():
    return 'hello world :)'
