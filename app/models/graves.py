# -*- coding: utf-8 -*-

from flask import current_app

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
        items = list(search.keys()) + [criteria]

        for k, v in search.items():
            if k in columns and v:
                if k == 'zone_id':
                    filters += (
                        db.or_(Zone.description.ilike('%' + v + '%'),
                               Zone.complement.ilike('%' + v + '%')), )
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            if criteria == 'zone_id':
                orders = (getattr(Zone.description, order)(), )
            else:
                orders = (getattr(getattr(cls, criteria), order)(), )

        if 'zone_id' in items:
            joins += (Zone, cls.zone_id == Zone.id, )

        return cls.query.join(*joins).filter(*filters).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        return {
            'id':
            self.id,
            'name': ('Rua {g.street} - Túmulo {g.number}').format(g=self)
        }

    def __repr__(self):
        return '{0}({1} {2})'.format(self.__class__.__name__, self.street,
                                     self.number)
