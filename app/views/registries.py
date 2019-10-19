# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.registries import COLUMNS, RegistryForm, RegistrySearchForm
from ..models import City, Registry

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

    if form.city_id.data:
        city = City.get_or_404(form.city_id.data)
        form.city_id.choices = [(city.id, f'{city.name} - {city.state.name}')]

    if form.validate() and request.method == 'POST':
        registry = Registry()
        form.populate_obj(registry)
        registry.save()
        return jsonify({'redirect': url_for('registries.index')})

    return render_template('registries/view.html',
                           title='Adicionar Cartório',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit(id):
    registry = Registry.get_or_404(id)
    form = RegistryForm(request.form, obj=registry)

    if form.city_id.data:
        city = City.get_or_404(form.city_id.data)
        form.city_id.choices = [(city.id, f'{city.name} - {city.state.name}')]

    if request.args.get('format', '', type=str) == 'view':
        return render_template('registries/view.html',
                               title='Cartório',
                               form=form,
                               view=True)

    if form.validate() and request.method == 'PUT':
        form.populate_obj(registry)
        registry.update()
        return jsonify({'redirect': url_for('registries.index')})

    return render_template('registries/view.html',
                           title='Editar Cartório',
                           form=form,
                           method='put',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Registry.get_or_404(id).delete()
    return '', 204
