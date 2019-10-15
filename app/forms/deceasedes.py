# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (DateField, FormField, RadioField, IntegerField,
                     SelectField, StringField, SubmitField)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import html5, TextArea

from ..utils.forms import MultiCheckboxField, SearchField
from ..models import CivilStates, Ethnicity

COLUMNS = [('name', 'Nome'), ('age', 'Idade'), ('birth_date', 'Data de Nascimento'), ('death_datetime', 'Data de Falecimento'), ('gender', 'Genero'), ('cause', 'Causa da Morte'), ('registration', 'registration'), ('number', 'Numero'), ('complement', 'Complemento'), ('birthplace', 'Local de Nascimento'), ('civil_state', 'Estado Civil'), ('home_address', 'Endereço da Casa'), ('death_address', 'Local do falecimento'), ('doctor', 'Medico'), ('ethnicity', 'Etnia'), ('grave', 'Tumulo'), ('registry', 'Cartorio'), ('childrens', 'Filiação')]
ORDERS = [('asc','Ascendente'), ('desc','Descente')]


class DeceasedForm(FlaskForm):

    name = StringField(
        'Nome',
        [InputRequired(message='Insira o Nome!'),
        Length(1, 255)])
    age = IntegerField(
        'Idade',
        [InputRequired(message='Insira a Idade!')],
        widget=html5.NumberInput(min=0))
    birth_date = DateField(
        'Data de Nascimento',
        [InputRequired(message='Insira a Data de Nascimento!'),
        Length(1, 255)])
    death_datetime = DateField(
        'Data de Falecimento',
        [InputRequired(message='Insira a Data de Falecimento!'),
        Length(1, 255)])
    gender = RadioField(
        'Genêro',
        [InputRequired(message='Insira o Genêro!')],
        choices=[('M', 'Masculino'), ('F', 'Feminino')])
    cause = StringField(
        'Causa da Morte',
        [InputRequired(message='Insira a Causa da Morte!'),
        Length(1, 1500)],
        widget=TextArea())
    registration = StringField(
        'Matrícula',
        [InputRequired(message='Insira a Matrícula!'),
        Length(1, 40)])
    birthplace = SelectField(
        'Local de Nascimento',
        [InputRequired(message='Insira o Local de Nascimento!')],
        choices=(), coerce=int)
    civil_state_id = SelectField(
        'Estado Civil',
        [InputRequired(message='Insira o Estado civil!')],
        choices=(), coerce=int)
    home_address_id = SelectField(
        'Endereço Residencial',
        [InputRequired('Selecione o Endereço Residencial')],
        choices=(), coerce=int)
    home_address_number = StringField(
        'Número', [Length(1, 5)])
    home_address_complement = StringField(
        'Complemento',
        [InputRequired(message='Insira o Complemento!'),
        Length(1, 255)])
    death_address_id = SelectField(
        'Endereço de Falecimento',
        [InputRequired('Selecione o Endereço de Falecimento')],
        choices=(), coerce=int)
    death_address_number = StringField(
        'Número', [Length(1, 5)])
    death_address_complement = StringField(
        'Complemento',
        [InputRequired(message='Insira o Complemento!'),
        Length(1, 255)])
    doctor_id = SelectField(
        'Medico',
        [InputRequired(message='Insira o nome do Médico!')],
        choices=(), coerce=int)
    ethnicity_id = SelectField(
        'Etnia',
        [InputRequired(message='Insira a Etnia!')],
        choices=(), coerce=int)
    grave = SelectField(
        'Tumulo',
        [InputRequired(message='Insira o Tumulo!')],
        choices=(), coerce=int)
    registry = SelectField(
        'Cartorio',
        [InputRequired(message='Insira o Cartorio!')],
        choices=(), coerce=int)
    childrens = SelectField(
        'Filiação',
        [InputRequired(message='Insira o Filiação!')],
        choices=(), coerce=int)
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(DeceasedForm, self).__init__(*args, **kwargs)
        self.ethnicity_id.choices = [(e.id, e.description)
                                     for e in Ethnicity.query.order_by(
                                         Ethnicity.description.asc()).all()]
        self.ethnicity_id.choices.insert(0, (0, ''))
        self.civil_state_id.choices = [(e.id, e.description)
                                     for e in CivilStates.query.order_by(
                                         CivilStates.description.asc()).all()]
        self.civil_state_id.choices.insert(0, (0, ''))


class DeceasedSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar falecido ...')
    filters = MultiCheckboxField('Filtros', choices=COLUMNS, default=['name'])
    clause = SelectField('Critério', choices=COLUMNS, default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
