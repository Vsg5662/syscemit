# -*- coding: utf-8 -*-

import csv
import os

from flask import current_app
from config import basedir

from ..extensions import db
from ..mixins import CRUDMixin
from .states import State


class City(CRUDMixin, db.Model):
    __tablename__ = 'cities'
    name = db.Column(db.String(40), nullable=False)
    state_id = db.Column(db.Integer,
                         db.ForeignKey('states.id'),
                         nullable=False)
    registries = db.relationship('Registry', backref='city', lazy='dynamic')
    deceased = db.relationship('Deceased', backref='city', lazy='dynamic')
    addresses = db.relationship('Address', backref='city', lazy='dynamic')

    @classmethod
    def fetch(cls, search, criteria, order, page):
        joins = filters_ = orders = ()

        if criteria and search:
            filters_ += (getattr(cls, criteria).ilike('%' + search + '%'), )
        elif search:
            filters_ += (cls.name.ilike('%' + search + '%'), )

        if criteria and order:
            orders += (getattr(getattr(cls, criteria), order)(), )
        else:
            orders += (cls.name.asc(), )
        return cls.query.join(*joins).filter(*filters_).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    @classmethod
    def populate(cls):
        states = {s.name: int(s.id) for s in State.query.all()}
        path = os.path.join(basedir, 'seeds', 'cities.tsv')
        with open(path) as f:
            reader = csv.DictReader(f, delimiter='\t')
            cities = [
                cls(name=row['CIDADE'], state_id=states[row['ESTADO']])
                for row in reader
            ]
        db.session.bulk_save_objects(cities)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': f'{self.name} - {self.state.uf}'
        }

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
