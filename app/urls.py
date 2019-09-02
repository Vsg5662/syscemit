# -*- coding: utf-8 -*-

from .views import main, users
from .utils.helpers import HandleError


def init_app(app):
    app.register_blueprint(main.bp)
    app.register_blueprint(users.bp)

    # errors
    errors = {
        403: u'Acesso Negado!',
        404: u'Página não Encontrada!',
        500: u'Erro Interno do Servidor!'
    }
    for code, message in errors.items():
        app.errorhandler(code)(HandleError('error.html', message))
