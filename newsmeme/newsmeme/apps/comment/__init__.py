#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Comment
from .forms import CommentForm
from flask import Blueprint
comment = Blueprint('comment', __name__, template_folder='templates')
