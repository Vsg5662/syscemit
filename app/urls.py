# -*- coding: utf-8 -*-

from .utils.helpers import HandleError
from .views import (addresses, auth, cities, deceased, doctors, graves, main,
                    registries, users, zones)


def init_app(app):
    app.register_blueprint(addresses.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(cities.bp)
    app.register_blueprint(deceased.bp)
    app.register_blueprint(doctors.bp)
    app.register_blueprint(graves.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(registries.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(zones.bp)

    # errors
    errors = {
        403: u'Acesso Negado!',
        404: u'Página não Encontrada!',
        500: u'Erro Interno do Servidor!'
    }
    for code, message in errors.items():
        app.errorhandler(code)(HandleError('error.html', message))
