# -*- coding: utf-8 -*-

from flask import Blueprint, abort, jsonify, request
from flask_login import login_required

from ..models.cities import City

bp = Blueprint('Cities', __name__, url_prefix='/cidades')


@bp.route('/')
@login_required
def cities():
    if not request.is_xhr:
        abort(404)
    search = request.args.get('search', '', type=str)
    pagination = City.fetch(search, '', '', 1)
    cities = pagination.items

    return jsonify({'result': [c.serialize() for c in cities]})
