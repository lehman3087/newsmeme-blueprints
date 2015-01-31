#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, Email
from flask.ext.babel import lazy_gettext as _


class ContactForm(Form):

    name = TextField(_("Your name"), validators=[
                     Required(message=_('Your name is required'))])

    email = TextField(_("Your email address"), validators=[
                      Required(message=_("Email address required")),
                      Email(message=_("A valid email address is required"))])

    subject = TextField(_("Subject"), validators=[
                        Required(message=_("Subject required"))])

    message = TextAreaField(_("Message"), validators=[
                            Required(message=_("Message required"))])

    submit = SubmitField(_("Send"))


class MessageForm(Form):

    subject = TextField(_("Subject"), validators=[
                        Required(message=_("Subject required"))])

    message = TextAreaField(_("Message"), validators=[
                            Required(message=_("Message required"))])

    submit = SubmitField(_("Send"))
