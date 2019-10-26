# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (IntegerField, FormField, SelectField,
                     StringField, SubmitField)
from wtforms.validators import InputRequired, Length

from ..models.cities import City
from ..utils.forms import get_fields, ORDERS


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

    def refill(cls):
        if cls.city_id.data:
            city = City.get(cls.city_id.data)
            cls.city_id.choices = [(city.id,
                                    '{c.name} - {c.state.uf}'.format(c=city))]


class RegistryHeadersForm(FlaskForm):
    name = StringField('Nome')
    city_id = StringField('Cidade')


class RegistrySearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    filters = FormField(RegistryHeadersForm)
    criteria = SelectField('Ordenar por',
                           choices=get_fields(RegistryHeadersForm),
                           default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
