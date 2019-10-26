# -*- coding: utf-8 -*-

import subprocess

import click
from flask.cli import AppGroup

from .extensions import db
from .models.addresses import Address
from .models.cities import City
from .models.civil_states import CivilState
from .models.deceased import Deceased
from .models.doctors import Doctor
from .models.ethnicities import Ethnicity
from .models.graves import Grave
from .models.registries import Registry
from .models.states import State
from .models.user_types import UserType
from .models.users import User
from .models.zones import Zone
from .utils.helpers import shell_context


def init_app(app):
    user_cli = AppGroup('user', help='Perform user management.')

    @app.shell_context_processor
    def make_shell_context():
        return shell_context(app, db, Address, City, CivilState, Deceased,
                             Doctor, Ethnicity, Grave, Registry, State, User,
                             UserType, Zone)

    @app.cli.command()
    def initdb():
        '''Initialize and populate the database.'''
        db.create_all()
        UserType.populate()
        State.populate()
        City.populate()
        Address.populate()
        CivilState.populate()
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
        '''Create a new user.'''
        User.create(name=name,
                    login=login,
                    password=password,
                    user_type_id=type)

    @user_cli.command()
    def list():
        '''List all users.'''
        print('{:<20}{:<20}{:<20}'.format('LOGIN', 'NAME', 'TYPE'))
        for u in User.query.all():
            print('{:<20}{:<20}{:<20}'.format(
                u.login, u.name, u.user_type.role))

    @user_cli.command()
    @click.confirmation_option(prompt='Do you really want to delete the user?')
    @click.option('-l', '--login', 'login', required=True, help='User login')
    def delete(login):
        '''Delete a user.'''
        u = User.query.filter_by(login=login).first()
        u.delete()

    @app.cli.command()
    def format():
        '''Format and organize code according to pep 8'''
        formaters = ['isort -vb -rc *.py app/', 'yapf -vv -r -i *.py app/']
        for f in formaters:
            print('[*] Running {}'.format(f.split()[0]))
            subprocess.call(f, shell=True)

    @app.cli.command()
    def lint():
        '''Verify the code quality.'''
        print('[*] Running Flake8')
        subprocess.call('flake8 *.py app/', shell=True)

    app.cli.add_command(user_cli)
