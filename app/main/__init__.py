#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Thejojo'

from flask import Blueprint
main = Blueprint('main', __name__)
from . import views,errors