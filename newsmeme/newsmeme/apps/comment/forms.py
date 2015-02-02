#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required
from flask.ext.babel import lazy_gettext as _


class CommentForm(Form):

    comment = TextAreaField(validators=[
                            Required(message=_("Comment is required"))])

    submit = SubmitField(_("Save"))
    cancel = SubmitField(_("Cancel"))


class CommentAbuseForm(Form):

    complaint = TextAreaField("Complaint", validators=[
                              Required(message=_("You must enter the details"
                                                 " of the complaint"))])

    submit = SubmitField(_("Send"))
