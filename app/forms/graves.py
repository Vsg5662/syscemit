# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..models.zones import Zone
from ..utils.forms import SearchField

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

    def refill(cls):
        if cls.zone_id.data:
            zone = Zone.get(cls.zone_id.data)
            cls.zone_id.choices = [
                (zone.id, '{z.description} - {z.complement}'.format(z=zone))
            ]


class GraveSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar túmulo ...')
    criteria = SelectField('Filtrar por', choices=COLUMNS, default='')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
