# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, Required

from ..utils.forms import MultiCheckboxField, SearchField

COLUMNS = [('street', 'Rua'), ('cep', 'CEP'), ('district', 'Bairro'),
           ('city', 'Cidade')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class AddressForm(FlaskForm):
    street = StringField(
        'Rua', [InputRequired(message='Insira a Rua!'),
                Length(1, 255)])
    cep = StringField('CEP',
                      [InputRequired(message='Insira a CEP!'),
                       Length(1, 255)])
    district = StringField(
        'Bairro', [InputRequired(message='Insira a Bairro!'),
                   Length(1, 255)])
    city_id = SelectField('Cidade',
                          [InputRequired(message='Selecione uma cidade!')],
                          choices=(),
                          coerce=int)
    submit = SubmitField('Salvar')


class AddressSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar endereço ...')
    filters = MultiCheckboxField('Filtros',
                                 choices=COLUMNS,
                                 default=['street'])
    clause = SelectField('Critério', choices=COLUMNS, default='street')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
