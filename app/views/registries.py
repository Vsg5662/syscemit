# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..forms.registries import RegistryForm, RegistrySearchForm
from ..models.registries import Registry

bp = Blueprint('registries', __name__, url_prefix='/cartorios')


@bp.route('/')
@login_required
def index():
    form = RegistrySearchForm(request.args)
    grid = request.args.get('grid', 0, type=bool)
    filters = form.filters.data
    criteria = form.criteria.data
    order = form.order.data
    pagination = Registry.fetch(filters, criteria, order, form.page.data)
    registries = pagination.items
    filters = {'filters-' + k: v for k, v in filters.items()}

    if request.is_xhr and not grid:
        return jsonify({'result': [r.serialize() for r in registries]})

    return render_template('registries/index.html',
                           icon='fa-books',
                           title='Cartórios',
                           clean_url=url_for('registries.index'),
                           create_url=url_for('registries.create'),
                           form=form,
                           filters=filters,
                           criteria=criteria,
                           order=order,
                           pagination=pagination,
                           registries=registries)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = RegistryForm()
    form.refill()

    if form.validate() and request.method == 'POST':
        registry = Registry()
        form.populate_obj(registry)
        registry.save()
        return jsonify({'redirect': url_for('registries.index')})

    return render_template('registries/view.html',
                           icon='fa-books',
                           title='Adicionar Cartório',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit(id):
    view = request.args.get('format', '', type=str)
    view = True if not current_user.is_admin() else view
    title = 'Cartório' if view == 'view' else 'Editar Cartório'

    registry = Registry.get_or_404(id)
    obj = {'obj': registry} if request.method == 'GET' else {}
    form = RegistryForm(**obj)
    form.refill()

    if form.validate() and current_user.is_admin() and request.method == 'PUT':
        form.populate_obj(registry)
        registry.update()
        return jsonify({'redirect': url_for('registries.index')})

    return render_template('registries/view.html',
                           icon='fa-books',
                           title=title,
                           form=form,
                           method='put',
                           color='warning',
                           view=bool(view))


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Registry.get_or_404(id).delete()
    return '', 204
