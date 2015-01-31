#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~~~

    Default configuration

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""

# from newsmeme import views


class DefaultConfig(object):

    """
    Default configuration for a newsmeme application.
    """

    DEBUG = True

    # change this in your production settings !!!

    SECRET_KEY = "secret"

    # keys for localhost. Change as appropriate.

    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'

    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % (
        'root', 'root', 'localhost', 'newsmeme')

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 30

    # 需要测试发送邮件功能的时候，自由设置！
    # 如果需要开启代码中向管理员发送邮件的功能的话，需要在 ADMINS 里面添加收件人
    # 如: ADMINS = ('admin@newsmeme.com')。默认情况下这个功能关闭
    ADMINS = ()

    MAIL_SERVER = u'mail.newsmeme.com'
    MAIL_USERNAME = u'service@newsmeme.com'
    MAIL_PASSWORD = u'123'
    DEFAULT_MAIL_SENDER = u'service@newsmeme.com'

    ACCEPT_LANGUAGES = ['en', 'fi']

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'

    THEME = 'newsmeme'

    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300


class TestConfig(object):

    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ECHO = False
