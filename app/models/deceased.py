from datetime import datetime
from re import findall, DOTALL

from flask import current_app

from .cities import City
from .graves import Grave
from .zones import Zone

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
    annotation = db.Column(db.String(1500))
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
        columns = cls.__table__.columns.keys() + ['zone_id']
        orders = ['asc', 'desc']
        items = []

        for k, v in search.items():
            if k in columns and v:
                if k == 'birthplace_id':
                    filters += (City.name.ilike('%' + v + '%'), )
                    items.append(k)
                elif (k == 'death_datetime' and
                      findall(r'^\d{4} \d{4}$', v, flags=DOTALL)):
                    v = list(map(int, v.split()))
                    v[0] = datetime(v[0], 1, 1)
                    v[1] = datetime(v[1], 12, 31)
                    filters += (cls.death_datetime >= v[0],
                                cls.death_datetime <= v[1], )
                elif k == 'grave_id':
                    if findall(r'^\w+ \w+$', v, flags=DOTALL):
                        v = v.split()
                        filters += (Grave.street.ilike('%' + v[0] + '%'),
                                    Grave.number.ilike('%' + v[1] + '%'), )
                    else:
                        filters += (Grave.street.ilike('%' + v + '%'), )
                    items.append(k)
                elif k == 'zone_id':
                    if findall(r'^\w+ \w+$', v, flags=DOTALL):
                        v = v.split()
                        filters += (Zone.description.ilike('%' + v[0] + '%'),
                                    Zone.complement.ilike('%' + v[1] + '%'), )
                    else:
                        filters += (Zone.description.ilike('%' + v + '%'), )
                    items.append(k)
                else:
                    filters += (getattr(cls, k).ilike('%' + v + '%'), )

        if criteria in columns and order in orders:
            if criteria == 'birthplace_id':
                orders = (getattr(City.name, order)(), )
                items.append(criteria)
            elif criteria == 'grave_id':
                orders = (getattr(Grave.number, order)(), )
                items.append(criteria)
            elif criteria == 'zone_id':
                orders = (getattr(Zone.description, order)(), )
                items.append(criteria)
            else:
                orders = (getattr(getattr(cls, criteria), order)(), )

        if 'birthplace_id' in items:
            joins += (City, )
            filters += (cls.birthplace_id == City.id, )

        if 'grave_id' in items or 'zone_id' in items:
            joins += (Grave, )
            filters += (cls.grave_id == Grave.id, )

        if 'zone_id' in items:
            joins += (Zone, )
            filters += (Grave.zone_id == Zone.id, )

        return cls.query.join(*joins).filter(*filters).order_by(
            *orders).paginate(page,
                              per_page=current_app.config['PER_PAGE'],
                              error_out=False)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)
