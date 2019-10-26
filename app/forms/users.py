# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (IntegerField, FormField, PasswordField,
                     SelectField, StringField, SubmitField)
from wtforms.validators import InputRequired, Length, Required

from ..models.user_types import UserType
from ..utils.forms import get_fields, ORDERS


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


class UserHeadersForm(FlaskForm):
    login = StringField('Login')
    name = StringField('Nome')
    user_type_id = StringField('Tipo de Usuário')


class UserSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    filters = FormField(UserHeadersForm)
    criteria = SelectField('Ordenar por',
                           choices=get_fields(UserHeadersForm),
                           default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
