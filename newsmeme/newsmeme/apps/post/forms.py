#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, TextAreaField, RadioField, SubmitField
from wtforms.validators import ValidationError, Required, Optional, URL
from flask.ext.babel import gettext, lazy_gettext as _

from newsmeme.extensions import db
from .models import Post


class PostForm(Form):

    title = TextField(_("Title of your post"), validators=[
                      Required(message=_("Title required"))])

    link = TextField(_("Link"), validators=[
                     Optional(),
                     URL(message=_("This is not a valid URL"))])

    description = TextAreaField(_("Description"))

    tags = TextField(_("Tags"))

    access = RadioField(_("Who can see this post ?"),
                        default=Post.PUBLIC,
                        coerce=int,
                        choices=((Post.PUBLIC, _("Everyone")),
                                 (Post.FRIENDS, _("Friends only")),
                                 (Post.PRIVATE, _("Just myself"))))

    submit = SubmitField(_("Save"))

    def __init__(self, *args, **kwargs):
        self.post = kwargs.get('obj', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def validate_link(self, field):
        posts = Post.query.public().filter_by(link=field.data)
        if self.post:
            posts = posts.filter(db.not_(Post.id == self.post.id))
        if posts.count():
            raise ValidationError(
                message=gettext("This link has already been posted"))
