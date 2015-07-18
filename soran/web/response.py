""":mod:`soran.web.response` --- soran API response functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import render_template


def render_ok(template_name, **kwargs):
    return render_template(template_name, **kwargs), 200


def render_bad_request(template_name, **kwargs):
    return render_template(template_name, **kwargs), 400
