#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~

    Helper functions for newsmeme

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
import markdown
import re
import urlparse
import functools

from datetime import datetime
from unidecode import unidecode
from flask import current_app, g

from flask.ext.babel import gettext, ngettext
from flask.ext.themes import render_theme_template

from newsmeme.extensions import cache

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug. From http://flask.pocoo.org/snippets/5/"""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return unicode(delim.join(result))


markdown = functools.partial(markdown.markdown,
                             safe_mode='remove',
                             output_format="html")


cached = functools.partial(cache.cached,
                           unless=lambda: g.user is not None)


def get_theme_name():
    return current_app.config['THEME']


def render_template(template, **context):
    return render_theme_template(get_theme_name(), template, **context)


def timesince(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    if default is None:
        default = gettext("just now")

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        singular = u"%%(num)d %s ago" % singular
        plural = u"%%(num)d %s ago" % plural

        return ngettext(singular, plural, num=period)

    return default


def domain(url):
    """
    Returns the domain of a URL e.g. http://reddit.com/ > reddit.com
    """
    rv = urlparse.urlparse(url).netloc
    if rv.startswith("www."):
        rv = rv[4:]
    return rv
