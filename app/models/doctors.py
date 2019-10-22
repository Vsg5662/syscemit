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
        joins = filters_ = orders = ()

        if criteria and search:
            filters_ += (getattr(cls, criteria).ilike('%' + search + '%'), )
        elif search:
            filters_ += (cls.name.ilike('%' + search + '%'), )

        if criteria and order:
            orders += (getattr(getattr(cls, criteria), order)(), )
        else:
            orders += (cls.name.asc(), )
        return cls.query.join(*joins).filter(*filters_).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def serialize(self):
        return {'id': self.id, 'name': f'{self.name} - {self.crm}'}

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
