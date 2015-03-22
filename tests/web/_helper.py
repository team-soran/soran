from werkzeug.datastructures import MultiDict


def formify(formdata):
    return MultiDict([(key, values) for key, values in formdata.items()])
