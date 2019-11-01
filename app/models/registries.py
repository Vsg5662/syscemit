# -*- coding: utf-8 -*-

from itertools import chain

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
        joins = filters = ()
        columns = cls.__table__.columns.keys()
        orders = ['asc', 'desc']
        items = []

        for k, v in search.items():
            if k in columns and v:
                if k == 'city_id':
                    filters += (City.name.ilike('%' + v + '%'), )
                    items.append(k)
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            if criteria == 'city_id':
                orders = (getattr(City.name, order)(), )
                items.append(k)
            else:
                orders = (getattr(getattr(cls, criteria), order)(), )

        if 'city_id' in items:
            joins += (City, )
            filters += (cls.city_id == City.id, )

        return cls.query.join(*joins).filter(*filters).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        name = ', '.join([self.name, self.city.serialize().get('name')])
        return {'id': self.id, 'name': name}

    @staticmethod
    def dump(pagination):
        headers = iter([('NOME', 'CIDADE')])
        data = ((r.name, r.city.serialize().get('name') if r.city else '')
                for r in pagination.query.all())
        return chain(headers, data)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
