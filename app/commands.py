# -*- coding: utf-8 -*-

import subprocess

from .models import (Address, Children, City, CivilStatus, Deceased, District,
                     Doctor, Ethnicity, Grave, Registry, State, Street, User,
                     UserType, Zone, db)
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

    @app.cli.command()
    def format():
        formaters = ['isort -vb -rc *.py app/', 'yapf -vv -r -i *.py app/']
        for f in formaters:
            print('Running {}'.format(f.split()[0]))
            subprocess.call(f, shell=True)
