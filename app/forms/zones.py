# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, Optional

from ..utils.forms import SearchField

COLUMNS = [('description', 'Descrição'), ('complement', 'Complemento')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class ZoneForm(FlaskForm):
    description = StringField(
        'Descricao',
        [InputRequired(message='Insira o nome do area!'),
         Length(1, 255)])
    complement = StringField('Complemento', [Optional(), Length(1, 20)])
    submit = SubmitField('Salvar')


class ZoneSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar area ...')
    criteria = SelectField('Filtrar por',
                           choices=COLUMNS,
                           default='description')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
