# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..utils.forms import SearchField

COLUMNS = [('street', 'Rua'), ('cep', 'CEP'), ('district', 'Bairro'),
           ('city', 'Cidade')]
ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class AddressForm(FlaskForm):
    street = StringField(
        'Rua', [InputRequired(message='Insira a Rua!'),
                Length(1, 255)])
    district = StringField(
        'Bairro', [InputRequired(message='Insira a Bairro!'),
                   Length(1, 255)])
    city_id = SelectField('Cidade',
                          [InputRequired(message='Selecione uma cidade!')],
                          choices=(),
                          coerce=int)
    cep = StringField('CEP',
                      [InputRequired(message='Insira a CEP!'),
                       Length(1, 255)])
    submit = SubmitField('Salvar')


class AddressSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar endereço ...')
    criteria = SelectField('Filtrar por', choices=COLUMNS, default='street')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
