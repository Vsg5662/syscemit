# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.graves import COLUMNS, GraveForm, GraveSearchForm
from ..models import Grave

bp = Blueprint('graves', __name__, url_prefix='/tumulos')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = GraveSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if filters_ and search:
        filters += tuple(
            getattr(Grave, f).ilike('%' + search + '%') for f in filters_)
    elif search:
        filters += (Grave.name.ilike('%' + search + '%'), )

    if order and clause:
        orders += (getattr(getattr(Grave, clause), order)(), )

    if not orders:
        orders += (Grave.name.asc(), )
    pagination = Grave.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    graves = pagination.items

    return render_template('graves/index.html',
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           graves=graves)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = GraveForm()
    if form.validate():
        grave = Grave()
        form.populate_obj(grave)
        grave.save()
        return jsonify({'redirect': url_for('graves.index')})
    return render_template('graves/view.html',
                           form=form,
                           method='post',
                           label='Adicionar Túmulo',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    grave = Grave.get_or_404(id)
    form = GraveForm(request.form, obj=grave)
    if form.validate():
        form.populate_obj(grave)
        grave.update()
        return jsonify({'redirect': url_for('graves.index')})
    return render_template('graves/view.html',
                           form=form,
                           method='put',
                           label='Editar Túmulo',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Grave.get_or_404(id).delete()
    return '', 204
