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
        joins = filters_ = orders = ()

        if criteria and search:
            if criteria == 'type':
                joins += (UserType, )
                filters_ += (
                    cls.user_type_id == UserType.id,
                    UserType.description.ilike('%' + search + '%'),
                )
                orders += (getattr(UserType.description, order)(), )
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
