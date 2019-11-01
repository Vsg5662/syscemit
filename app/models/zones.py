# -*- coding: utf-8 -*-

from itertools import chain
from re import DOTALL, findall

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
                if (k == 'description'
                        and findall(r'^\w+ \w+$', v, flags=DOTALL)):
                    v = v.split()
                    filters += (
                        cls.description.ilike('%' + v[0] + '%'),
                        cls.complement.ilike('%' + v[1] + '%'),
                    )
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            orders = (getattr(getattr(cls, criteria), order)(), )

        return cls.query.filter(*filters).order_by(*orders).paginate(
            page, per_page=current_app.config['PER_PAGE'], error_out=False)

    def serialize(self):
        name = [self.description]
        if self.complement:
            name.append(self.complement)
        return {'id': self.id, 'name': ' - '.join(name)}

    @staticmethod
    def dump(pagination):
        headers = iter([('DESCRIÇÃO', 'COMPLEMENTO')])
        data = ((z.description, z.complement) for z in pagination.query.all())
        return chain(headers, data)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.description)
