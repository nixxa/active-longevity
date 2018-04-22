# -*- coding: utf-8 -*-
import json

from flask import request, url_for
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import load_only
from urllib.parse import urlparse, urljoin

from models import Activity


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj): #pylint: disable=E0202
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def filter_by_form(query, form):
    """
    Generate query by form filters
    """
    if form.category.data is not None and form.category.data != 'None':
        query = query.filter_by(category=form.category.data)
    if form.name.data is not None and form.name.data != 'None':
        query = query.filter_by(name=form.name.data)
    if form.district.data is not None and form.district.data != 'None':
        query = query.filter_by(district=form.district.data)
    if form.executor.data is not None and form.executor.data != 'None':
        query = query.filter_by(executor=form.executor.data)
    return query


def fill_filter_form(form):
    """
    Apply form data to filter
    """
    query = Activity.query.options(load_only('category', 'name', 'district', 'executor')).all()
    form.category.choices = [('None', 'все')] + \
        [(x, x) for x in sorted(set([row.category for row in query]))]
    form.name.choices = [('None', 'все')] + \
        [(x, x) for x in sorted(set([row.name for row in query]))]
    form.district.choices = [('None', 'все')] + \
        [(x, x) for x in sorted(set([row.district for row in query]))]
    form.executor.choices = [('None', 'все')] + \
        [(x, x) for x in sorted(set([row.executor for row in query]))]


def is_safe_url(target):
    """
    Check if url safe
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    """
    Return redirect target
    """
    for target in request.values.get('next'), request.full_path:
        if not target:
            continue
        if is_safe_url(target):
            return target
