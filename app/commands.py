# -*- coding: utf-8 -*-

from .models import (Address, Children, City, CivilStatus, Deceased, District,
                     Doctor, Ethnicity, Grave, Registry, State,
                     Street, User, UserType, Zone, db)
from .utils.helpers import shell_context


def init_app(app):
    @app.shell_context_processor
    def make_shell_context():
        return shell_context(app, db, Address, Children, City, CivilStatus,
                             Deceased, District, Doctor, Ethnicity, Grave,
                             Registry, State, Street, User, UserType, Zone)

    @app.cli.command()
    def initdb():
        db.create_all()
        UserType.populate()
        State.populate()
        City.populate()
        CivilStatus.populate()
        Ethnicity.populate()
