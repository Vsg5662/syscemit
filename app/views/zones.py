# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.zones import COLUMNS, ZoneForm, ZoneSearchForm
from ..models import Zone

bp = Blueprint('zones', __name__, url_prefix='/regioes')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = ZoneSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if filters_ and search:
        filters += tuple(
            getattr(Zone, f).ilike('%' + search + '%') for f in filters_)
    elif search:
        filters += (Zone.description.ilike('%' + search + '%'), )

    if order and clause:
        orders += (getattr(getattr(Zone, clause), order)(), )

    if not orders:
        orders += (Zone.description.asc(), )
    pagination = Zone.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    zones = pagination.items
    if request.is_xhr:
        return jsonify({
            'result': [{
                'id': z.id,
                'name': f'{z.description} - {z.complement}'
            } for z in zones]
        })

    return render_template('zones/index.html',
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           zones=zones)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = ZoneForm()

    if form.validate() and request.method == 'POST':
        doctor = Zone()
        form.populate_obj(doctor)
        doctor.save()
        return jsonify({'redirect': url_for('zones.index')})

    return render_template('zones/view.html',
                           form=form,
                           method='post',
                           label='Adicionar Região',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    doctor = Zone.get_or_404(id)
    form = ZoneForm(request.form, obj=doctor)

    if form.validate() and request.method == 'PUT':
        form.populate_obj(doctor)
        doctor.update()
        return jsonify({'redirect': url_for('zones.index')})

    return render_template('zones/view.html',
                           form=form,
                           method='put',
                           label='Editar Região',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Zone.get_or_404(id).delete()
    return '', 204
