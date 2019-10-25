# -*- coding: utf-8 -*-

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def init_app(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Autentique-se para acessar esta página'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    from .utils.filters import strftime
    app.jinja_env.filters['strftime'] = strftime

    from .models.users import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
