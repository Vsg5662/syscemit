# -*- coding: utf-8 -*-

from flask import current_app

from ..extensions import db
from ..mixins import CRUDMixin


class Doctor(CRUDMixin, db.Model):
    __tablename__ = 'doctors'
    name = db.Column(db.String(255), nullable=False)
    crm = db.Column(db.String(20), nullable=False)
    deceased = db.relationship('Deceased', backref='doctors', lazy='dynamic')

    @classmethod
    def fetch(cls, search, criteria, order, page):
        filters = ()
        columns = cls.__table__.columns.keys()
        orders = ['asc', 'desc']

        for k, v in search.items():
            if k in columns and v:
                filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            orders = (getattr(getattr(cls, criteria), order)(), )

        return cls.query.filter(db.or_(*filters)).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        return {'id': self.id, 'name': '{s.name} - CRM {s.crm}'.format(s=self)}

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
