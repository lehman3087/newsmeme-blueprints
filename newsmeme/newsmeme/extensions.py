#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.mail import Mail
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

__all__ = ['oid', 'mail', 'db', 'cache']

oid = OpenID()
mail = Mail()
db = SQLAlchemy()
cache = Cache()

