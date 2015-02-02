#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import User
from flask import Blueprint
user = Blueprint('user', __name__, template_folder='templates')

