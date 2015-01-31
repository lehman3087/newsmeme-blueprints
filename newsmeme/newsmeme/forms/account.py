#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, TextField,\
    PasswordField, SubmitField
from wtforms.validators import ValidationError, Required, Email, EqualTo
from flask.ext.babel import gettext, lazy_gettext as _

from newsmeme.models import User
from newsmeme.extensions import db

from .validators import is_username


class LoginForm(Form):

    next = HiddenField()

    remember = BooleanField(_("Remember me"))

    login = TextField(_("Username or Email address"), validators=[
                      Required(message=_("You must provide an Email or username"))])

    password = PasswordField(_("Password"))

    submit = SubmitField(_("Login"))


class SignupForm(Form):

    next = HiddenField()

    username = TextField(_("Username"), validators=[
                         Required(message=_("Username Required")),
                         is_username])

    password = PasswordField(_("Password"), validators=[
                             Required(message=_("Password Required"))])

    password_again = PasswordField(_("Password again"), validators=[
                                   EqualTo("password", message=_("Passwords don't match"))])

    email = TextField(_("Email address"), validators=[
                      Required(message=_("Email address Required")),
                      Email(message=_("A valid Email address is Required"))])

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


class EditAccountForm(Form):

    username = TextField("Username", validators=[
                         Required(_("Username is Required")), is_username])

    email = TextField(_("Your Email address"), validators=[
                      Required(message=_("Email address Required")),
                      Email(message=_("A valid Email address is Required"))])

    receive_email = BooleanField(_("Receive private Emails from friends"))

    email_alerts = BooleanField(_("Receive an Email when somebody replies "
                                  "to your post or comment"))

    submit = SubmitField(_("Save"))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(EditAccountForm, self).__init__(*args, **kwargs)

    def validate_username(self, field):
        user = User.query.filter(db.and_(
                                 User.username.like(field.data),
                                 db.not_(User.id == self.user.id))).first()

        if user:
            raise ValidationError(message=gettext("This username is taken"))

    def validate_email(self, field):
        user = User.query.filter(db.and_(
                                 User.email.like(field.data),
                                 db.not_(User.id == self.user.id))).first()
        if user:
            raise ValidationError(message=gettext("This Email is taken"))


class RecoverPasswordForm(Form):

    email = TextField("Your Email address", validators=[
                      Email(message=_("A valid Email address is Required"))])

    submit = SubmitField(_("Find password"))


class ChangePasswordForm(Form):

    activation_key = HiddenField()

    password = PasswordField("Password", validators=[
                             Required(message=_("Password is Required"))])

    password_again = PasswordField(_("Password again"), validators=[
                                   EqualTo("password", message=_("Passwords don't match"))])

    submit = SubmitField(_("Save"))


class DeleteAccountForm(Form):

    recaptcha = RecaptchaField(_("Copy the words appearing below"))

    submit = SubmitField(_("Delete"))
