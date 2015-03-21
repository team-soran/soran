from flask import Flask

from . import user
from .converter import YoutubeConverter

app = Flask(__name__)
app.register_blueprint(user.bp, url_prefix='/users')


app.url_map.converters.update(
    youtube=YoutubeConverter
)

@app.route('/', methods=['GET'])
def hello():
    return 'hello world :)'
