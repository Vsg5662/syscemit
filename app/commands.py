# -*- coding: utf-8 -*-

import subprocess

import click
from flask.cli import AppGroup

from .models import (Address, City, CivilStates, Deceased, Doctor, Ethnicity,
                     Filiation, Grave, Registry, State, User, UserType, Zone,
                     db)
from .utils.helpers import shell_context


def init_app(app):
    user_cli = AppGroup('user')

    @app.shell_context_processor
    def make_shell_context():
        return shell_context(app, db, Address, Filiation, City, CivilStates,
                             Deceased, Doctor, Ethnicity, Grave, Registry,
                             State, User, UserType, Zone)

    @app.cli.command()
    def initdb():
        db.create_all()
        UserType.populate()
        State.populate()
        City.populate()
        CivilStates.populate()
        Ethnicity.populate()

    @user_cli.command()
    @click.option('-n', '--name', 'name', required=True, help='Your name')
    @click.option('-l', '--login', 'login', required=True, help='Your login')
    @click.option('-p',
                  '--password',
                  'password',
                  prompt=True,
                  required=True,
                  hide_input=True,
                  confirmation_prompt=True,
                  help='Your password')
    @click.option('-t',
                  '--type',
                  'type',
                  required=True,
                  type=int,
                  help='Your user type: 1 (admin), 2(employee)')
    def create(name, login, password, type):
        User.create(name=name,
                    login=login,
                    password=password,
                    user_type_id=type)

    @app.cli.command()
    def format():
        formaters = ['isort -vb -rc *.py app/', 'yapf -vv -r -i *.py app/']
        for f in formaters:
            print('Running {}'.format(f.split()[0]))
            subprocess.call(f, shell=True)

    app.cli.add_command(user_cli)
