# -*- coding: utf-8 -*-

import csv
import os

from config import basedir

from ..extensions import db
from ..mixins import CRUDMixin


class State(CRUDMixin, db.Model):
    __tablename__ = 'states'
    name = db.Column(db.String(20), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    cities = db.relationship('City', backref='state', lazy='dynamic')

    @classmethod
    def populate(cls):
        path = os.path.join(basedir, 'seeds', 'states.tsv')
        with open(path) as f:
            reader = csv.DictReader(f, delimiter='\t')
            states = [cls(name=row['ESTADO'], uf=row['UF']) for row in reader]
        db.session.bulk_save_objects(states)
        db.session.commit()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
