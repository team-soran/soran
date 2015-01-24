from flask import Flask

from . import user

version = 1

app = Flask(__name__)
app.register_blueprint(user.bp, url_prefix='/{}/users'.format(version))

@app.route('/', methods=['GET'])
def hello():
    return 'hello world :)'
