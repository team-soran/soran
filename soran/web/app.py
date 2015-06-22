""":mod:`soran.web.app` --- soran web app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Flask, render_template
from sassutils.wsgi import SassMiddleware

from . import user, youtube
from .converter import YoutubeConverter


app = Flask(__name__)


app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'soran.web': ('static/sass', 'static/css', '/static/css')
})


def import_python(module_name: str):
    modules = module_name.split(':')
    if len(modules) != 2:
        return None
    try:
        return getattr(__import__(modules[0]), modules[1])
    except (ImportError, AttributeError):
        return None


app.add_template_global(import_python, 'import_python')
app.add_template_global(isinstance, 'isinstance')


app.url_map.converters.update(
    youtube=YoutubeConverter
)


app.register_blueprint(user.bp)
app.register_blueprint(youtube.bp)


@app.route('/', methods=['GET'])
def hello():
    """메인 핸들러

    :return:
    """
    return render_template('hello.html')
