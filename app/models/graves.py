# -*- coding: utf-8 -*-

import csv
import os

from itertools import chain
from re import DOTALL, findall

from flask import current_app

from config import basedir
from ..extensions import db
from ..mixins import CRUDMixin
from .zones import Zone


class Grave(CRUDMixin, db.Model):
    __tablename__ = 'graves'
    street = db.Column(db.String(5), nullable=False)
    number = db.Column(db.String(5), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    deceased = db.relationship('Deceased', backref='grave', lazy='dynamic')

    @classmethod
    def fetch(cls, search, criteria, order, page):
        joins = filters = ()
        columns = cls.__table__.columns.keys()
        orders = ['asc', 'desc']
        items = []

        for k, v in search.items():
            if k in columns and v:
                if (k == 'street' and findall(r'^\w+ \w+$', v, flags=DOTALL)):
                    v = v.split()
                    filters += (
                        cls.street.ilike('%' + v[0] + '%'),
                        cls.number.ilike('%' + v[1] + '%'),
                    )
                elif k == 'zone_id':
                    if v.isnumeric():
                        filters += (cls.zone_id == v, )
                    elif findall(r'^\w+ \w+$', v, flags=DOTALL):
                        v = v.split()
                        filters += (
                            Zone.description.ilike('%' + v[0] + '%'),
                            Zone.complement.ilike('%' + v[1] + '%'),
                        )
                    else:
                        filters += (Zone.description.ilike('%' + v + '%'), )
                    items.append(k)
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            if criteria == 'zone_id':
                orders = (getattr(Zone.description, order)(), )
                items.append(criteria)
            else:
                orders = (db.func.length(getattr(cls, criteria)), )
                orders += (getattr(getattr(cls, criteria), order)(), )

        if 'zone_id' in items:
            joins += (Zone, )
            filters += (cls.zone_id == Zone.id, )

        return cls.query.join(*joins).filter(*filters).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        name = []
        if self.street:
            name.append('Rua ' + self.street)
        if self.number:
            name.append('Túmulo ' + self.number)

        return {'id': self.id, 'name': ' - '.join(name)}

    @classmethod
    def populate(cls):
        zones = {
            z.description + '-' + z.complement: int(z.id)
            for z in Zone.query.all()
        }
        path = os.path.join(basedir, 'seeds', 'graves.tsv')
        with open(path) as f:
            reader = csv.DictReader(f, delimiter='\t')
            graves = [
                cls(street=row['RUA'],
                    number=row['NÚMERO'],
                    zone_id=zones[row['REGIÃO'] + '-' + row['COMPLEMENTO']])
                for row in reader
            ]
        db.session.bulk_save_objects(graves)
        db.session.commit()

    @staticmethod
    def dump(pagination):
        headers = iter([('RUA', 'NÚMERO', 'REGIÃO')])
        data = ((g.street, g.number,
                 g.zone.serialize().get('name') if g.zone else '')
                for g in pagination.query.all())
        return chain(headers, data)

    def __repr__(self):
        return '{0}({1} {2})'.format(self.__class__.__name__, self.street,
                                     self.number)
