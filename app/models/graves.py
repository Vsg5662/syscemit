# -*- coding: utf-8 -*-

from re import findall, DOTALL

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
        items = []

        for k, v in search.items():
            if k in columns and v:
                if (k == 'street' and
                        findall(r'^\w+ \w+$', v, flags=DOTALL)):
                    v = v.split()
                    filters += (cls.street.ilike('%' + v[0] + '%'),
                                cls.number.ilike('%' + v[1] + '%'), )
                elif k == 'zone_id':
                    if v.isnumeric():
                        filters += (cls.zone_id == v, )
                    elif findall(r'^\w+ \w+$', v, flags=DOTALL):
                        v = v.split()
                        filters += (Zone.description.ilike('%' + v[0] + '%'),
                                    Zone.complement.ilike('%' + v[1] + '%'), )
                    else:
                        filters += (Zone.description.ilike('%' + v + '%'), )
                    items.append(k)
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            if criteria == 'zone_id':
                orders = (getattr(Zone.description, order)(), )
                items.append(criteria)
            else:
                orders = (getattr(getattr(cls, criteria), order)(), )

        if 'zone_id' in items:
            joins += (Zone, )
            filters += (cls.zone_id == Zone.id, )

        return cls.query.join(*joins).filter(*filters).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        name = []
        if self.street:
            name.append('Rua ' + self.street)
        if self.number:
            name.append('Túmulo ' + self.number)

        return {'id': self.id, 'name': ' - '.join(name)}

    def __repr__(self):
        return '{0}({1} {2})'.format(self.__class__.__name__, self.street,
                                     self.number)
