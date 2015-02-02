#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required
from flask.ext.babel import lazy_gettext as _


class MessageForm(Form):

    subject = TextField(_("Subject"), validators=[
                        Required(message=_("Subject required"))])

    message = TextAreaField(_("Message"), validators=[
                            Required(message=_("Message required"))])

    submit = SubmitField(_("Send"))
