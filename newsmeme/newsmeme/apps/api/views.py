#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request

from newsmeme.apps.api import api
from newsmeme.apps.post import Post
from newsmeme.apps.user import User
from newsmeme.helpers import cached


@api.route("/post/<int:post_id>/")
@cached()
def post(post_id):

    post = Post.query.public().filter_by(id=post_id).first_or_404()

    return jsonify(**post.json)


@api.route("/search/")
def search():

    keywords = request.args.get("keywords", "")

    if not keywords:
        return jsonify(results=[])

    num_results = int(request.args.get("num_results", 20))

    if num_results > 100:
        num_results = 100

    posts = Post.query.search(keywords).public().limit(num_results)

    return jsonify(results=list(posts.jsonify()))


@api.route("/user/<username>/")
@cached()
def user(username):

    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author_id=user.id).public()

    return jsonify(posts=list(posts.jsonify()))
