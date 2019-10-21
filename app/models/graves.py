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
            filters_ += (cls.street.ilike('%' + search + '%'), )

        if not orders:
            orders += (cls.street.asc(), )
        return cls.query.join(*joins).filter(*filters_).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def __repr__(self):
        return '{0}({1} {2})'.format(self.__class__.__name__, self.street,
                                     self.number)
