# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..utils.forms import MultiCheckboxField, SearchField

COLUMNS = [('name', 'Nome'), ('crm', 'CRM')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class DoctorForm(FlaskForm):
    name = StringField(
        'Nome',
        [InputRequired(message='Insira o nome do médico!'),
         Length(1, 255)])
    crm = StringField(
        'CRM',
        [InputRequired(message='Insira o CRM do médico!'),
         Length(1, 20)])
    submit = SubmitField('Salvar')


class DoctorSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar médico ...')
    filters = MultiCheckboxField('Filtros', choices=COLUMNS, default=['name'])
    clause = SelectField('Critério', choices=COLUMNS, default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
