# -*- coding: utf-8 -*-

from flask import Flask

from . import commands, extensions, urls


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)

    extensions.init_app(app)
    commands.init_app(app)
    urls.init_app(app)

    return app
