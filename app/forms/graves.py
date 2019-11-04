# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (FormField, IntegerField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import InputRequired, Length

from ..models.zones import Zone
from ..utils.forms import ORDERS, get_fields


class GraveForm(FlaskForm):
    street = StringField(
        'Rua', [InputRequired(message='Insira a rua do túmulo!'),
                Length(1, 255)])
    number = StringField(
        'Número', [InputRequired(message='Insira o número do túmulo!'),
                   Length(1, 255)])
    zone_id = SelectField('Região',
                          [InputRequired(message='Selecione uma região!')],
                          choices=(),
                          coerce=int)
    submit = SubmitField('Salvar')

    def refill(cls):
        if cls.zone_id.data:
            zone = Zone.get_or_404(cls.zone_id.data)
            cls.zone_id.choices = [tuple(zone.serialize().values())]


class GraveHeadersForm(FlaskForm):
    street = StringField('Rua')
    number = StringField('Número')
    zone_id = StringField('Região')


class GraveSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    filters = FormField(GraveHeadersForm)
    criteria = SelectField('Ordenar por',
                           choices=get_fields(GraveHeadersForm),
                           default='street')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
