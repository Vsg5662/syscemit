# -*- coding: utf-8 -*-

import csv
import os

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

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
