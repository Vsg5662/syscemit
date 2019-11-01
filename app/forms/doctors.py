# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (FormField, IntegerField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import InputRequired, Length

from ..utils.forms import ORDERS, get_fields


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


class DoctorHeadersForm(FlaskForm):
    name = StringField('Nome')
    crm = StringField('CRM')


class DoctorSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    filters = FormField(DoctorHeadersForm)
    criteria = SelectField('Ordenar por',
                           choices=get_fields(DoctorHeadersForm),
                           default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
