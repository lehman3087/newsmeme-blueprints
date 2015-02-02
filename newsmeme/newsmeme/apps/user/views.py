#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import url_for, g, redirect, flash, current_app

from flask.ext.mail import Message
from flask.ext.babel import gettext as _

from newsmeme.helpers import render_template, cached
from newsmeme.apps.user import user

from newsmeme.apps.post import Post
from newsmeme.apps.comment import Comment
from newsmeme.decorators import keep_login_url
from newsmeme.extensions import mail
from newsmeme.permissions import auth
from .forms import MessageForm
from .models import User


@user.route("/message/<int:user_id>/", methods=("GET", "POST"))
@auth.require(401)
def send_message(user_id):

    user = User.query.get_or_404(user_id)
    user.permissions.send_message.test(403)

    form = MessageForm()

    if form.validate_on_submit():

        body = render_template("emails/send_message.html",
                               user=user,
                               subject=form.subject.data,
                               message=form.message.data)

        subject = _("You have received a message from %(name)s",
                    name=g.user.username)

        message = Message(subject=subject,
                          body=body,
                          sender=current_app.config.get(
                              'DEFAULT_MAIL_SENDER'),
                          recipients=[user.email])

        mail.send(message)

        flash(_("Your message has been sent to %(name)s",
                name=user.username), "success")

        return redirect(url_for("user.posts", username=user.username))

    return render_template("send_message.html", user=user, form=form)


@user.route("/<username>/")
@user.route("/<username>/<int:page>/")
@cached()
@keep_login_url
def posts(username, page=1):

    user = User.query.filter_by(username=username).first_or_404()

    page_obj = Post.query.filter_by(author=user).restricted(g.user).\
        as_list().paginate(page, Post.PER_PAGE)

    page_url = lambda page: url_for('user.posts',
                                    username=username,
                                    page=page)

    num_comments = Comment.query.filter_by(author_id=user.id).\
        restricted(g.user).count()

    return render_template("posts.html",
                           user=user,
                           num_posts=page_obj.total,
                           num_comments=num_comments,
                           page_obj=page_obj,
                           page_url=page_url)


@user.route("/<username>/comments/")
@user.route("/<username>/comments/<int:page>/")
@cached()
@keep_login_url
def comments(username, page=1):

    user = User.query.filter_by(username=username).first_or_404()

    page_obj = Comment.query.filter_by(author=user).\
        order_by(Comment.id.desc()).restricted(g.user).\
        paginate(page, Comment.PER_PAGE)

    page_url = lambda page: url_for('user.comments',
                                    username=username,
                                    page=page)

    num_posts = Post.query.filter_by(author_id=user.id).\
        restricted(g.user).count()

    return render_template("comments.html",
                           user=user,
                           num_posts=num_posts,
                           num_comments=page_obj.total,
                           page_obj=page_obj,
                           page_url=page_url)


@user.route("/<username>/followers/")
@user.route("/<username>/followers/<int:page>/")
@cached()
@keep_login_url
def followers(username, page=1):

    user = User.query.filter_by(username=username).first_or_404()

    num_posts = Post.query.filter_by(author_id=user.id).\
        restricted(g.user).count()

    num_comments = Comment.query.filter_by(author_id=user.id).\
        restricted(g.user).count()

    followers = user.get_followers().order_by(User.username.asc())

    return render_template("followers.html",
                           user=user,
                           num_posts=num_posts,
                           num_comments=num_comments,
                           followers=followers)


@user.route("/<username>/following/")
@user.route("/<username>/following/<int:page>/")
@cached()
@keep_login_url
def following(username, page=1):

    user = User.query.filter_by(username=username).first_or_404()

    num_posts = Post.query.filter_by(author_id=user.id).\
        restricted(g.user).count()

    num_comments = Comment.query.filter_by(author_id=user.id).\
        restricted(g.user).count()

    following = user.get_following().order_by(User.username.asc())

    return render_template("following.html",
                           user=user,
                           num_posts=num_posts,
                           num_comments=num_comments,
                           following=following)
