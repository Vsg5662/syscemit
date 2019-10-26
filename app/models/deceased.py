from flask import current_app

from .cities import City
from .graves import Grave

from ..extensions import db
from ..mixins import CRUDMixin


class Deceased(CRUDMixin, db.Model):
    __tablename__ = 'deceased'
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    birth_date = db.Column(db.Date)
    death_datetime = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    home_address_number = db.Column(db.String(5))
    home_address_complement = db.Column(db.String(255))
    filiations = db.Column(db.String(512))
    registration = db.Column(db.String(40), nullable=False)
    cause = db.Column(db.String(1500), nullable=False)
    death_address_number = db.Column(db.String(5))
    death_address_complement = db.Column(db.String(255))
    birthplace_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    civil_state_id = db.Column(db.Integer, db.ForeignKey('civil_states.id'))
    ethnicity_id = db.Column(db.Integer,
                             db.ForeignKey('ethnicities.id'),
                             nullable=False)
    home_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    death_address_id = db.Column(db.Integer,
                                 db.ForeignKey('addresses.id'),
                                 nullable=False)
    doctor_id = db.Column(db.Integer,
                          db.ForeignKey('doctors.id'),
                          nullable=False)
    grave_id = db.Column(db.Integer,
                         db.ForeignKey('graves.id'),
                         nullable=False)
    registry_id = db.Column(db.Integer,
                            db.ForeignKey('registries.id'),
                            nullable=False)

    @classmethod
    def fetch(cls, search, criteria, order, page):
        joins = filters = ()
        columns = cls.__table__.columns.keys()
        orders = ['asc', 'desc']
        items = list(search.keys()) + [criteria]

        if 'birthplace_id' in items:
            joins += (City, )

        if 'grave_id' in items:
            joins += (Grave, )

        for k, v in search.items():
            if k in columns and v:
                if k == 'birthplace_id':
                    filters += (cls.birthplace_id == City.id,
                                City.name.ilike('%' + v + '%'), )
                elif k == 'grave_id':
                    filters += (cls.grave_id == Grave.id,
                                db.or_(Grave.street.ilike('%' + v + '%'),
                                       Grave.number.ilike('%' + v + '%')), )
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            if criteria == 'birthplace_id':
                orders = (getattr(City.name, order)(), )
            elif criteria == 'grave_id':
                orders = (getattr(Grave.number, order)(), )
            else:
                orders = (getattr(getattr(cls, criteria), order)(), )

        return cls.query.join(*joins).filter(*filters).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
