# -*- coding: utf-8 -*-

import csv
import os

import whoosh

from flask import current_app
from flask_whooshee import AbstractWhoosheer

from config import basedir

from ..extensions import db, search
from ..mixins import CRUDMixin
from .cities import City


@search.register_model('street', 'district', 'cep')
class Address(CRUDMixin, db.Model):
    __tablename__ = 'addresses'
    street = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    home_address = db.relationship('Deceased',
                                   foreign_keys='Deceased.home_address_id',
                                   backref='address_home',
                                   lazy='dynamic')
    death_address = db.relationship('Deceased',
                                    foreign_keys='Deceased.death_address_id',
                                    backref='address_death',
                                    lazy='dynamic')

    @classmethod
    def retrieve(cls, search, page):
        return cls.query.whooshee_search(search).paginate(
            page,
            per_page=current_app.config['PER_PAGE'],
            error_out=False)

    @classmethod
    def fetch(cls, search, criteria, order, page):
        joins = filters_ = orders = ()

        if criteria and search:
            if criteria == 'city':
                joins += (City, )
                filters_ += (
                    cls.city_id == City.id,
                    City.name.ilike('%' + search + '%'),
                )
                orders += (getattr(City.name, order)(), )
            else:
                filters_ = (getattr(cls, criteria).ilike('%' + search + '%'), )
                orders += (getattr(getattr(cls, criteria), order)(), )
        elif search:
            filters_ += (cls.street.ilike('%' + search + '%'), )

        if not orders:
            orders += (cls.street.asc(), )
        return cls.query.join(*joins).filter(*filters_).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    @classmethod
    def populate(cls):
        cities = {
            c.name + ' - ' + c.state.uf: int(c.id)
            for c in City.query.all()
        }
        path = os.path.join(basedir, 'seeds', 'streets.tsv')
        with open(path) as f:
            reader = csv.DictReader(f, delimiter='\t')
            cities = [
                cls(street=row['RUA'],
                    district=row['BAIRRO'],
                    cep=row['CEP'],
                    city_id=cities[row['CIDADE'] + ' - ' + row['ESTADO']])
                for row in reader
            ]
        db.session.bulk_save_objects(cities)
        db.session.commit()

    def serialize(self):
        return {
            'id':
            self.id,
            'name': ('{a.street} - {a.district},'
                     ' {a.city.name} - {a.city.state.uf},'
                     ' CEP {a.cep}').format(a=self)
        }

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.street)


@search.register_whoosheer
class AddressCityWhoosheer(AbstractWhoosheer):
    schema = whoosh.fields.Schema(
        address_id=whoosh.fields.NUMERIC(stored=True, unique=True),
        city_id=whoosh.fields.NUMERIC(stored=True),
        cityname=whoosh.fields.TEXT(),
        street=whoosh.fields.TEXT(),
        district=whoosh.fields.TEXT(),
        cep=whoosh.fields.TEXT())

    models = [Address, City]

    @classmethod
    def update_city(cls, writer, city):
        pass

    @classmethod
    def update_address(cls, writer, address):
        writer.update_document(address_id=address.id,
                               city_id=address.city.id,
                               cityname=address.city.name,
                               street=address.street,
                               district=address.district,
                               cep=address.cep)

    @classmethod
    def insert_city(cls, writer, city):
        pass

    @classmethod
    def insert_address(cls, writer, address):
        writer.add_document(address_id=address.id,
                            city_id=address.city.id,
                            cityname=address.city.name,
                            street=address.street,
                            district=address.district,
                            cep=address.cep)

    @classmethod
    def delete_city(cls, writer, city):
        pass

    @classmethod
    def delete_address(cls, writer, address):
        writer.delete_by_term('address_id', address.id)
