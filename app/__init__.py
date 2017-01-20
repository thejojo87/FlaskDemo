#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Thejojo'

from flask import Flask

from flask_bootstrap import Bootstrap
# 日期和时间-3.6
from flask_moment import Moment


# 数据库-5-5
from flask_sqlalchemy import SQLAlchemy


# 电子邮件-6
from flask_mail import Mail

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

