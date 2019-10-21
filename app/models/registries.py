# -*- coding: utf-8 -*-

from flask import current_app

from ..extensions import db
from ..mixins import CRUDMixin
from .cities import City


class Registry(CRUDMixin, db.Model):
    __tablename__ = 'registries'
    name = db.Column(db.String(255), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    deceased = db.relationship('Deceased', backref='registry', lazy='dynamic')

    @classmethod
    def fetch(cls, search, criteria, order, page):
        joins = filters_ = orders = ()

        if criteria and search:
            if criteria == 'city':
                joins += (City, )
                filters_ += (
                    cls.city_id == City.id,
                    City.name.ilike('%' + search + '%'),
                )
                orders += (getattr(City.name, order)(), )
            else:
                filters_ = (getattr(cls, criteria).ilike('%' + search + '%'), )
                orders += (getattr(getattr(cls, criteria), order)(), )
        elif search:
            filters_ += (cls.name.ilike('%' + search + '%'), )

        if not orders:
            orders += (cls.name.asc(), )
        return cls.query.join(*joins).filter(*filters_).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
