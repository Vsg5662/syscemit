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
        joins = filters_ = orders = ()
        print('#'*50)
        print(search, criteria, order, page)
        print('#'*50)

        if criteria and search:
            if criteria == 'zone':
                joins += (Zone, )
                filters_ += (
                    cls.zone_id == Zone.id,
                    Zone.description.ilike('%' + search + '%'),
                )
                orders += (getattr(Zone.description, order)(), )
            else:
                filters_ = (getattr(cls, criteria).ilike('%' + search + '%'), )
                orders += (getattr(getattr(cls, criteria), order)(), )
        elif search:
            search = search.lower().split()
            joins += (Zone, )
            filters_ += (cls.zone_id == Zone.id, db.or_(
                db.func.lower(Grave.street).in_(search),
                db.func.lower(Grave.number).in_(search),
                db.func.lower(Zone.description).in_(search),
                db.func.lower(Zone.complement).in_(search)), )

        if not orders:
            orders += (cls.street.asc(), )
        return cls.query.join(*joins).filter(*filters_).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        return {
            'id':
            self.id,
            'name': ('{g.zone.description} - {g.zone.complement}, '
                     'Rua {g.street} - Túmulo {g.number}').format(g=self)
        }

    def __repr__(self):
        return '{0}({1} {2})'.format(self.__class__.__name__, self.street,
                                     self.number)
