import os

from annotation.typed import typechecked


@typechecked
def read_config(filename: str) -> dict:
    path = os.environ.get('SORAN_CONFIG', None) or filename
    config = {}
    if path is None:
        raise Exception('configuration not found')
    with open(path) as config_file:
        exec(compile(config_file.read(), filename, 'exec'), config)
    return dict((k, v) for k, v in config.items() if k.isupper())
