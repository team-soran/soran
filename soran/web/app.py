from flask import Flask

from . import user
from .converter import YoutubeConverter

app = Flask(__name__)


def import_python(module_name):
    modules = module_name.split(':')
    if len(modules) != 2:
        return None
    try:
        return getattr(__import__(modules[0]), modules[1])
    except (ImportError, AttributeError):
        return None


def python_isinstance(obj, cls):
    if not cls or type(cls) is not type:
        return False
    return isinstance(obj, cls)


app.add_template_global(import_python, 'import_python')
app.add_template_global(python_isinstance, 'isinstance')


app.url_map.converters.update(
    youtube=YoutubeConverter
)


app.register_blueprint(user.bp, url_prefix='/users')


@app.route('/', methods=['GET'])
def hello():
    return 'hello world :)'
