# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (FormField, IntegerField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import InputRequired, Length

from ..models.cities import City
from ..utils.forms import ORDERS, get_fields


class AddressForm(FlaskForm):
    street = StringField(
        'Rua', [InputRequired(message='Insira a rua do endereço!'),
                Length(1, 255)])
    district = StringField(
        'Bairro', [InputRequired(message='Insira o bairro do endereço!'),
                   Length(1, 255)])
    city_id = SelectField('Cidade',
                          [InputRequired(
                              message='Selecione a cidade do endereço!')],
                          choices=(),
                          coerce=int)
    cep = StringField('CEP',
                      [InputRequired(message='Insira o CEP do endereço!'),
                       Length(1, 255)])
    submit = SubmitField('Salvar')

    def refill(cls):
        if cls.city_id.data:
            city = City.get(cls.city_id.data)
            cls.city_id.choices = [(city.id,
                                    '{c.name} - {c.state.uf}'.format(c=city))]


class AddressHeadersForm(FlaskForm):
    street = StringField('Rua')
    cep = StringField('CEP')
    district = StringField('Bairro')
    city_id = StringField('Cidade')


class AddressSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    filters = FormField(AddressHeadersForm)
    criteria = SelectField('Ordenar por',
                           choices=get_fields(AddressHeadersForm),
                           default='street')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
