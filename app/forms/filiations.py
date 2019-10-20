# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..utils.forms import SearchField

COLUMNS = [('name', 'Nome')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class FiliationForm(FlaskForm):
    name = StringField(
        'Nome',
        [InputRequired(message='Insira o nome do parente!'),
         Length(1, 255)])

    submit = SubmitField('Salvar')


class FiliationSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar Parentes ...')
    criteria = SelectField('Filtrar por', choices=COLUMNS, default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
