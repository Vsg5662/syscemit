# -*- coding: utf-8 -*-

from flask import current_app

from ..extensions import db
from ..mixins import CRUDMixin


class Zone(CRUDMixin, db.Model):
    __tablename__ = 'zones'
    description = db.Column(db.String(40), nullable=False)
    complement = db.Column(db.String(10))
    graves = db.relationship('Grave', backref='zone', lazy='dynamic')

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

        return cls.query.filter(*filters).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': '{s.description} - {s.complement}'.format(s=self)
        }

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.description)
