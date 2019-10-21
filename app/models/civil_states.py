# -*- coding: utf-8 -*-
#
from ..extensions import db
from ..mixins import CRUDMixin


class CivilState(CRUDMixin, db.Model):
    __tablename__ = 'civil_states'
    description = db.Column(db.String(15), nullable=False)
    deceased = db.relationship('Deceased',
                               backref='civil_states',
                               lazy='dynamic')

    @classmethod
    def populate(cls):
        civil_states = [
            'Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)',
            'Separado(a)'
        ]
        civil_states = [cls(description=e) for e in civil_states]
        db.session.bulk_save_objects(civil_states)
        db.session.commit()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.description)
