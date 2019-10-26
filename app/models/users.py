# -*- coding: utf-8 -*-

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..mixins import CRUDMixin
from .user_types import UserType


class User(CRUDMixin, UserMixin, db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(30), nullable=False)
    _pwd_hash = db.Column(db.String(255), nullable=False)
    user_type_id = db.Column(db.Integer,
                             db.ForeignKey('user_types.id'),
                             nullable=False)

    @classmethod
    def fetch(cls, search, criteria, order, page):
        joins = filters = ()
        columns = cls.__table__.columns.keys()
        orders = ['asc', 'desc']
        items = list(search.keys()) + [criteria]

        for k, v in search.items():
            if k in columns and v:
                if k == 'user_type_id':
                    filters += (UserType.description.ilike('%' + v + '%'), )
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            if criteria == 'user_type_id':
                orders = (getattr(UserType.description, order)(), )
            else:
                orders = (getattr(getattr(cls, criteria), order)(), )

        if 'user_type_id' in items:
            joins += (UserType, cls.user_type_id == UserType.id, )

        return cls.query.join(*joins).filter(*filters).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._pwd_hash, password)

    def is_admin(self):
        return self.user_type.role == 'admin'

    def has_permissions(self, *roles):
        return self.user_type.role in roles

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.login)
