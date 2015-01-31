#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, TextField, SubmitField
from wtforms.validators import ValidationError, Required, Email, URL
from flask.ext.babel import gettext, lazy_gettext as _
from newsmeme.models import User
from .validators import is_username


class OpenIdSignupForm(Form):

    next = HiddenField()

    username = TextField(_("Username"), validators=[
                         Required(_("Username Required")),
                         is_username])

    email = TextField(_("Email address"), validators=[
                      Required(message=_("Email address Required")),
                      Email(message=_("Valid Email address Required"))])

    recaptcha = RecaptchaField(_("Copy the words appearing below"))

    submit = SubmitField(_("Signup"))

    def validate_username(self, field):
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError(message=gettext("This username is taken"))

    def validate_email(self, field):
        user = User.query.filter(User.email.like(field.data)).first()
        if user:
            raise ValidationError(message=gettext("This Email is taken"))


class OpenIdLoginForm(Form):

    next = HiddenField()

    openid = TextField("OpenID", validators=[
                       Required(_("OpenID is Required")),
                       URL(_("OpenID must be a valid URL"))])

    submit = SubmitField(_("Login"))
