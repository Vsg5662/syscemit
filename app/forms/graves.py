# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..utils.forms import MultiCheckboxField, SearchField

COLUMNS = [('street', 'Rua'), ('number', 'Número'), ('zone', 'Região')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class GraveForm(FlaskForm):
    street = StringField(
        'Rua', [InputRequired(message='Insira a rua!'),
                Length(1, 255)])
    number = StringField(
        'Número', [InputRequired(message='Insira o Número!'),
                   Length(1, 255)])
    zone_id = SelectField('Região',
                          [InputRequired(message='Selecione uma região!')],
                          choices=(),
                          coerce=int)
    submit = SubmitField('Salvar')


class GraveSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar túmulo ...')
    filters = MultiCheckboxField('Filtros',
                                 choices=COLUMNS,
                                 default=['street'])
    clause = SelectField('Critério', choices=COLUMNS, default='street')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
