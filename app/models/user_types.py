# -*- coding: utf-8 -*-

from ..extensions import db
from ..mixins import CRUDMixin


class UserType(CRUDMixin, db.Model):
    __tablename__ = 'user_types'
    description = db.Column(db.String(25), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    users = db.relationship('User', backref='user_type', lazy='dynamic')

    @classmethod
    def populate(cls):
        user_types = [('Administrador', 'admin'), ('Funcionário', 'employee')]
        user_types = [cls(description=d, role=r) for d, r in user_types]
        db.session.bulk_save_objects(user_types)
        db.session.commit()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.description)
