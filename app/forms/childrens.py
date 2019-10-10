# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..utils.forms import MultiCheckboxField, SearchField

COLUMNS = [('name', 'Nome')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class ChildrenForm(FlaskForm):
    name = StringField(
        'Nome',
        [InputRequired(message='Insira o nome do filho!'),
         Length(1, 255)])

    submit = SubmitField('Salvar')


class ChildrenSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar filho ...')
    filters = MultiCheckboxField('Filtros', choices=COLUMNS, default=['name'])
    clause = SelectField('Critério', choices=COLUMNS, default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
