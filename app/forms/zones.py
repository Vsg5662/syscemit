# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..utils.forms import MultiCheckboxField, SearchField

COLUMNS = [('description', 'Descricao'), ('complement', 'Complemento')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class ZoneForm(FlaskForm):
    description = StringField(
        'Descricao',
        [InputRequired(message='Insira o nome do area!'),
         Length(1, 255)])
    complement = StringField('Complemento', [
        InputRequired(message='Insira o Complemento do area!'),
        Length(1, 20)
    ])
    submit = SubmitField('Salvar')


class ZoneSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar area ...')
    filters = MultiCheckboxField('Filtros',
                                 choices=COLUMNS,
                                 default=['description'])
    clause = SelectField('Critério', choices=COLUMNS, default='description')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
