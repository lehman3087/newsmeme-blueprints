#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .forms import PostForm
from .models import Post, Tag
from flask import Blueprint
post = Blueprint('post', __name__, template_folder='templates')
