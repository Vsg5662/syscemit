# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, Required

from ..models import UserType


class UserForm(FlaskForm):
    login = StringField(
        'Login',
        [InputRequired(message='Insira o login do usuário!'),
         Length(1, 30)])
    name = StringField(
        'Nome',
        [InputRequired(message='Insira o nome do usuário!'),
         Length(1, 255)])
    password = PasswordField(
        'Senha', [InputRequired(message='Insira a senha do usuário!')])
    user_type_id = SelectField(
        'Tipo de Usuário', [Required(message='Selecione um tipo de usuário')],
        coerce=int)
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user_type_id.choices = [(u.id, u.description)
                                     for u in UserType.query.all()]
        self.user_type_id.choices.insert(0, (0, ''))


class UserLoginForm(FlaskForm):
    login = StringField('Login', [InputRequired(message='Login inválido!')])
    password = PasswordField('Senha',
                             [InputRequired(message='Insira a senha!')])
    submit = SubmitField('Entrar')
