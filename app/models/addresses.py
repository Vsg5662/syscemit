# -*- coding: utf-8 -*-

import csv
import os
from itertools import chain

from flask import current_app

from config import basedir

from ..extensions import db
from ..mixins import CRUDMixin
from .cities import City


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
    def fetch(cls, search, criteria, order, page):
        joins = filters = ()
        columns = cls.__table__.columns.keys()
        orders = ['asc', 'desc']
        items = []

        for k, v in search.items():
            if k in columns and v:
                if k == 'city_id':
                    if v.isnumeric():
                        filters += (cls.city_id == v, )
                    else:
                        filters += (City.name.ilike('%' + v + '%'), )
                    items.append(k)
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            if criteria == 'city_id':
                orders = (getattr(City.name, order)(), )
                items.append(criteria)
            else:
                orders = (getattr(getattr(cls, criteria), order)(), )

        if 'city_id' in items:
            joins += (City, )
            filters += (cls.city_id == City.id, )

        return cls.query.join(*joins).filter(*filters).order_by(
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
        name = ' - '.join([self.street, self.district])
        if self.cep:
            name += ', CEP ' + self.cep

        return {'id': self.id, 'name': name}

    @staticmethod
    def dump(pagination):
        headers = iter([('RUA', 'BAIRRO', 'CEP', 'CIDADE', 'ESTADO')])
        data = ((a.street, a.district, a.cep, a.city.name, a.city.state.uf)
                for a in pagination.query.all())
        return chain(headers, data)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.street)
