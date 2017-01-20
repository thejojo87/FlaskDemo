#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Thejojo'

# 表单类-4-2
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')