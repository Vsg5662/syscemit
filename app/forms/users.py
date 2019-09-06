# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length


class UserLoginForm(FlaskForm):
    login = StringField('Login', [InputRequired(message='Login inválido!')])
    password = PasswordField('Senha',
                             [InputRequired(message='Insira a senha!')])
    submit = SubmitField('Entrar')
