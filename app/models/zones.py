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
        joins = filters_ = orders = ()

        if criteria and search:
            filters_ += (getattr(cls, criteria).ilike('%' + search + '%'), )
        elif search:
            filters_ += (cls.description.ilike('%' + search + '%'), )

        if criteria and order:
            orders += (getattr(getattr(cls, criteria), order)(), )
        else:
            orders += (cls.description.asc(), )
        return cls.query.join(*joins).filter(*filters_).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': f'{self.description} - {self.complement}'
        }

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.description)
