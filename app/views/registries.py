# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.registries import COLUMNS, RegistryForm, RegistrySearchForm
from ..models import Registry

bp = Blueprint('registries', __name__, url_prefix='/cartorios')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = RegistrySearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if filters_ and search:
        filters += tuple(
            getattr(Registry, f).ilike('%' + search + '%') for f in filters_)
    elif search:
        filters += (Registry.name.ilike('%' + search + '%'), )

    if order and clause:
        orders += (getattr(getattr(Registry, clause), order)(), )

    if not orders:
        orders += (Registry.name.asc(), )
    pagination = Registry.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    registries = pagination.items

    return render_template('registries/index.html',
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           registries=registries)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = RegistryForm()
    if form.validate():
        doctor = Registry()
        form.populate_obj(doctor)
        doctor.save()
        return jsonify({'redirect': url_for('registries.index')})
    return render_template('registries/view.html',
                           form=form,
                           method='post',
                           label='Adicionar Cartório',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    doctor = Registry.get_or_404(id)
    form = RegistryForm(request.form, obj=doctor)
    if form.validate():
        form.populate_obj(doctor)
        doctor.update()
        return jsonify({'redirect': url_for('registries.index')})
    return render_template('registries/view.html',
                           form=form,
                           method='put',
                           label='Editar Cartório',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Registry.get_or_404(id).delete()
    return '', 204
