# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import DateField, BooleanField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ..utils.forms import MultiCheckboxField, SearchField

COLUMNS = [('name', 'Nome'), ('age', 'Idade'), ('birth_date', 'Data de Nascimento'), ('death_datetime', 'Data de Falecimento'), ('gender', 'Genero'), ('cause', 'Causa da Morte'), ('registration', 'registration'), ('number', 'Numero'), ('complement', 'Complemento'), ('birthplace', 'Local de Nascimento'), ('civil_state', 'Estado Civil'), ('home_address', 'Endereço da Casa'), ('death_address', 'Local do falecimento'), ('doctor', 'Medico'), ('ethnicity', 'Etnia'), ('grave', 'Tumulo'), ('registry', 'Cartorio'), ('childrens', 'Filiação')]
ORDERS = [('asc','Ascendente'), ('desc','Descente')]


class DeceasedForm(FlaskForm):

    name = StringField(
        'Nome',
        [InputRequired(message='Insira o Nome!'),
        Length(1, 255)])
    age = IntegerField(
        'Idade',
        [InputRequired(message='Insira a Idade!')])
    birth_date = DateField(
        'Data de Nascimento',
        [InputRequired(message='Insira a Data de Nascimento!'),
        Length(1, 255)])
    death_datetime = DateField(
        'Data de Falecimento',
        [InputRequired(message='Insira a Data de Falecimento!'),
        Length(1, 255)])
    gender = BooleanField(
        'Genero',
        [InputRequired(message='Insira o Genero!')])
    cause = StringField(
        'Causa da Morte',
        [InputRequired(message='Insira a causa da morte!'),
        Length(1, 1500)])
    registration = StringField(
        'registration',
        [InputRequired(message='Insira o Cartorio!'),
        Length(1, 40)])
    number = StringField(
        'Numero',
        [InputRequired(message='Insira o Numero!'),
        Length(1, 5)])
    complement = StringField(
        'Complemento',
        [InputRequired(message='Insira o Complemento!'),
        Length(1, 255)])
    birthplace = SelectField(
        'Local de Nascimento',
        [InputRequired(message='Insira o Local de Nascimento!')],
        choices=(), coerce=int)
    civil_state = SelectField(
        'Estado Civil',
        [InputRequired(message='Insira o Estado civil!')],
        choices=(), coerce=int)
    home_address = SelectField(
        'Endereço da Casa',
        [InputRequired(message='Insira o Endereço da residencia!')],
        choices=(), coerce=int)
    death_address = SelectField(
        'Local do falecimento',
        [InputRequired(message='Insira o Local de falecimento!')],
        choices=(), coerce=int)
    doctor = SelectField(
        'Medico',
        [InputRequired(message='Insira o nome do Medico!')],
        choices=(), coerce=int)
    ethnicity = SelectField(
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



class DeceasedSearchForm(FlaskForm):
    page = IntegerField('Página', default=1)
    search = SearchField('Buscar falecido ...')
    filters = MultiCheckboxField('Filtros', choices=COLUMNS, default=['name'])
    clause = SelectField('Critério', choices=COLUMNS, default='name')
    order = SelectField('Ordem', choices=ORDERS, default='asc')
