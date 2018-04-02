# -*- coding: utf-8 -*-
"""
Jinja2 extentions
"""
from flask import request, url_for

def register_extentions(app):
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
