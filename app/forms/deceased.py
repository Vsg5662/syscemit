# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (DateField, DateTimeField, FormField, IntegerField,
                     RadioField, SelectField, StringField, SubmitField)
from wtforms.validators import InputRequired, Length, Optional
from wtforms.widgets import TextArea
from wtforms.widgets.html5 import NumberInput

from ..models.addresses import Address
from ..models.cities import City
from ..models.civil_states import CivilState
from ..models.doctors import Doctor
from ..models.ethnicities import Ethnicity
from ..models.graves import Grave
from ..models.registries import Registry
from ..utils.forms import get_fields, ORDERS


class DeceasedForm(FlaskForm):
    name = StringField('Nome', [Optional(), Length(1, 255)])
    registration = StringField(
        'Matrícula do Óbito',
        [InputRequired(message='Insira a Matrícula!'),
         Length(1, 40)])
    gender = RadioField('Genêro', [InputRequired(message='Insira o Genêro!')],
                        choices=[('M', 'Masculino'), ('F', 'Feminino')])
    ethnicity_id = SelectField('Etnia',
                               [InputRequired(message='Insira a Etnia!')],
                               choices=(),
                               coerce=int)
    civil_state_id = SelectField('Estado Civil', [Optional()],
                                 choices=(),
                                 coerce=int)
    age = IntegerField('Idade', [Optional()], widget=NumberInput(min=0))
    birth_date = DateField('Data de Nascimento', [Optional()],
                           format='%d/%m/%Y')
    birthplace_id = SelectField('Naturalidade', [Optional()],
                                choices=(),
                                coerce=int)
    filiations = StringField('Filiação', [Optional(), Length(1, 255)])
    home_city_id = SelectField('Cidade', [Optional()],
                               choices=(),
                               coerce=int)
    home_address_id = SelectField('Endereço Residencial', [Optional()],
                                  choices=(),
                                  coerce=int)
    home_address_number = StringField('Número', [Optional(), Length(1, 5)])
    home_address_complement = StringField(
        'Complemento', [Optional(), Length(1, 255)])
    death_datetime = DateTimeField(
        'Data de Falecimento',
        [InputRequired(message='Insira a Data de Falecimento!')],
        format='%d/%m/%Y %H:%M')
    death_city_id = SelectField('Cidade', [Optional()],
                                choices=(),
                                coerce=int)
    death_address_id = SelectField(
        'Endereço de Falecimento',
        [InputRequired('Selecione o Endereço de Falecimento')],
        choices=(),
        coerce=int)
    death_address_number = StringField('Número', [Optional(), Length(1, 5)])
    death_address_complement = StringField(
        'Complemento', [Optional(), Length(1, 255)])
    cause = StringField(
        'Causa da Morte',
        [InputRequired(message='Insira a Causa da Morte!'),
         Length(1, 1500)],
        widget=TextArea())
    zone_id = SelectField('Região',
                          [InputRequired('Insira a região')],
                          choices=(),
                          coerce=int)
    grave_id = SelectField('Túmulo',
                           [InputRequired(message='Insira o Tumulo!')],
                           choices=(),
                           coerce=int)
    doctor_id = SelectField(
        'Médico', [InputRequired(message='Insira o nome do Médico!')],
        choices=(),
        coerce=int)
    registry_id = SelectField('Cartório',
                              [InputRequired(message='Insira o Cartório!')],
                              choices=(),
                              coerce=int)
    annotation = StringField(
        'Observações / Averbações',
        [Optional(),
         Length(1, 1500)],
        widget=TextArea())
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(DeceasedForm, self).__init__(*args, **kwargs)
        self.ethnicity_id.choices = [(e.id, e.description)
                                     for e in Ethnicity.query.order_by(
                                         Ethnicity.description.asc()).all()]
        self.ethnicity_id.choices.insert(0, (0, ''))
        self.civil_state_id.choices = [(e.id, e.description)
                                       for e in CivilState.query.order_by(
                                           CivilState.description.asc()).all()]
        self.civil_state_id.choices.insert(0, (0, ''))

    def refill(cls):
        if cls.birthplace_id.data:
            city = City.get_or_404(cls.birthplace_id.data)
            cls.birthplace_id.choices = [tuple(city.serialize().values())]

        if cls.home_address_id.data:
            address = Address.get_or_404(cls.home_address_id.data)
            cls.home_address_id.choices = [
                tuple(address.serialize().values())]
            cls.home_city_id.data = address.city.id
            cls.home_city_id.choices = [
                tuple(address.city.serialize().values())]

        if cls.death_address_id.data:
            address = Address.get_or_404(cls.death_address_id.data)
            cls.death_address_id.choices = [
                tuple(address.serialize().values())]
            cls.death_city_id.data = address.city.id
            cls.death_city_id.choices = [
                tuple(address.city.serialize().values())]

        if cls.doctor_id.data:
            doctor = Doctor.get_or_404(cls.doctor_id.data)
            cls.doctor_id.choices = [tuple(doctor.serialize().values())]

        if cls.grave_id.data:
            grave = Grave.get_or_404(cls.grave_id.data)
            cls.grave_id.choices = [tuple(grave.serialize().values())]
            if grave.zone_id:
                cls.zone_id.data = grave.zone.id
                cls.zone_id.choices = [tuple(grave.zone.serialize().values())]

        if cls.registry_id.data:
            registry = Registry.get_or_404(cls.registry_id.data)
            cls.registry_id.choices = [tuple(registry.serialize().values())]


class DeceasedHeadersForm(FlaskForm):
    name = StringField('Nome')
    birthplace_id = StringField('Naturalidade')
    death_datetime = StringField('Data de Falecimento')
    zone_id = StringField('Região')
    grave_id = StringField('Túmulo')


class DeceasedSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    filters = FormField(DeceasedHeadersForm)
    criteria = SelectField('Ordenar por',
                           choices=get_fields(DeceasedHeadersForm),
                           default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
