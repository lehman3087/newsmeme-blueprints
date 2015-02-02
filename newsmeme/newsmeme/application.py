#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    application.py
    ~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging

from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, request, g, jsonify, redirect, url_for, flash

from flask.ext.babel import Babel, gettext as _
from flask.ext.themes import setup_themes
from flask.ext.principal import Principal, identity_loaded

from werkzeug import import_string
from newsmeme import helpers
from newsmeme.config import DefaultConfig
from newsmeme.apps.user import User
from newsmeme.apps.post import Tag
from newsmeme.helpers import render_template
from newsmeme.extensions import db, mail, oid, cache

__all__ = ["create_app"]

DEFAULT_APP_NAME = "newsmeme"

DEFAULT_BLUEPRINTS = (
    ("newsmeme.apps.frontend", "frontend", ""),
    ("newsmeme.apps.post", "post", "/post"),
    ("newsmeme.apps.user", "user", "/user"),
    ("newsmeme.apps.comment", "comment", "/comment"),
    ("newsmeme.apps.account", "account", "/acct"),
    ("newsmeme.apps.feeds", "feeds", "/feeds"),
    ("newsmeme.apps.openid", "openid", "/openid"),
    ("newsmeme.apps.api", "api", "/api"),
)


def create_app(config=None, app_name=None, blueprints=None):

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)

    configure_app(app, config)

    configure_logging(app)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_before_handlers(app)
    configure_template_filters(app)
    configure_context_processors(app)
    # configure_after_handlers(app)
    configure_blueprints(app, blueprints)

    return app


def configure_app(app, config):

    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG', silent=True)


def configure_template_filters(app):

    @app.template_filter()
    def timesince(value):
        return helpers.timesince(value)


def configure_before_handlers(app):

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)


def configure_context_processors(app):

    @app.context_processor
    def get_tags():
        tags = cache.get("tags")
        if tags is None:
            tags = Tag.query.order_by(Tag.num_posts.desc()).limit(10).all()
            cache.set("tags", tags)

        return dict(tags=tags)

    @app.context_processor
    def config():
        return dict(config=app.config)


def configure_extensions(app):

    mail.init_app(app)
    db.init_app(app)
    oid.init_app(app)
    cache.init_app(app)

    setup_themes(app, app_identifier='newsmeme')

    # more complicated setups

    configure_identity(app)
    configure_i18n(app)


def configure_identity(app):

    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)


def configure_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES',
                                          ['en_gb'])

        return request.accept_languages.best_match(accept_languages)


def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed'))
        return render_template("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        _register_blueprint(app, blueprint)


def _register_blueprint(app, blueprint):

    if len(blueprint) is not 3:
        raise SyntaxError('BLUEPRINTS Invalid syntax!!!')
    path, name, prefix = blueprint

    try:
        packet = import_string(path + ".views")
    except Exception, msg:
        raise ImportError('import blueprint fail!!! %s' % msg)
    modules_name = getattr(packet, name, None)
    if not modules_name:
        app.logger.error("import blueprint %s from %s failed!\n" %
                         (name, packet + ".views"))
        raise ImportError("import blueprint %s from %s failed!\n" %
                          (name, packet + ".views"))
    if prefix:
        app.register_blueprint(modules_name, url_prefix=prefix)
    else:
        app.register_blueprint(modules_name)


def configure_logging(app):
    if app.debug or app.testing:
        return

    mail_handler = \
        SMTPHandler(app.config['MAIL_SERVER'],
                    'error@newsmeme.com',
                    app.config['ADMINS'],
                    'application error',
                    (
                        app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'],
        ))

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path,
                             app.config['DEBUG_LOG'])

    debug_file_handler = \
        RotatingFileHandler(debug_log,
                            maxBytes=100000,
                            backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path,
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)
