# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired


class AuthLoginForm(FlaskForm):
    login = StringField('Login',
                        [InputRequired(message='Um login é requerido!')])
    password = PasswordField('Senha',
                             [InputRequired(message='Uma senha é requerida!')])
    submit = SubmitField('Entrar')
