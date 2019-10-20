# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import InputRequired, Length, Required

from ..models import UserType
from ..utils.forms import SearchField

COLUMNS = [('name', 'Nome'), ('login', 'Login'), ('type', 'Tipo')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


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


class UserSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar usuários ...')
    criteria = SelectField('Filtrar por', choices=COLUMNS, default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
