# -*- coding: utf-8 -*-

from flask import Blueprint, abort, current_app, jsonify, request
from flask_login import login_required

from ..models import City

bp = Blueprint('Cities', __name__, url_prefix='/cidades')

@bp.route('/')
@login_required
def cities():
    if not request.is_xhr:
        abort(404)
    search = request.args.get('search')
    filters = ()
    if search:
        filters += (City.name.like('%'+search+'%'),)
    cities = City.query.filter(*filters).order_by(
        City.name.asc()).all()
    return jsonify({
        'cities': [{
            'id': c.id,
            'name': c.name,
            'state': c.state.name,
        } for c in cities]
    })
