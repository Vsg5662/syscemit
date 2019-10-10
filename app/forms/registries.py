# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..utils.forms import MultiCheckboxField, SearchField

COLUMNS = [('name', 'Nome'), ('city', 'Cidade')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class RegistryForm(FlaskForm):
    name = StringField(
        'Nome',
        [InputRequired(message='Insira o nome do cartório!'),
         Length(1, 255)])
    city_id = SelectField('Cidade',
                          [InputRequired(message='Selecione uma cidade!')],
                          choices=(),
                          coerce=int)
    submit = SubmitField('Salvar')


class RegistrySearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar cartório ...')
    filters = MultiCheckboxField('Filtros', choices=COLUMNS, default=['name'])
    clause = SelectField('Critério', choices=COLUMNS, default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
