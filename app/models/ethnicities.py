# -*- coding: utf-8 -*-

from ..extensions import db
from ..mixins import CRUDMixin


class Ethnicity(CRUDMixin, db.Model):
    __tablename__ = 'ethnicities'
    description = db.Column(db.String(10), nullable=False)
    deceased = db.relationship('Deceased', backref='ethnicity', lazy='dynamic')

    @classmethod
    def populate(cls):
        ethnicities = ['Branca', 'Parda', 'Negra', 'Indígena', 'Amarela']
        ethnicities = [cls(description=e) for e in ethnicities]
        db.session.bulk_save_objects(ethnicities)
        db.session.commit()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.description)
