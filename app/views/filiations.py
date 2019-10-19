# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.filiations import COLUMNS, FiliationForm, FiliationSearchForm
from ..models import Filiation

bp = Blueprint('filiations', __name__, url_prefix='/filiacao')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = FiliationSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if filters_ and search:
        filters += tuple(
            getattr(Filiation, f).ilike('%' + search + '%') for f in filters_)
    elif search:
        filters += (Filiation.name.ilike('%' + search + '%'), )

    if order and clause:
        orders += (getattr(getattr(Filiation, clause), order)(), )

    if not orders:
        orders += (Filiation.name.asc(), )
    pagination = Filiation.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    filiations = pagination.items

    return render_template('filiations/index.html',
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           filiations=filiations)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = FiliationForm()

    if form.validate():
        filiation = Filiation()
        form.populate_obj(filiation)
        filiation.save()
        return jsonify({'redirect': url_for('filiations.index')})

    return render_template('filiations/view.html',
                           form=form,
                           method='post',
                           label='Adicionar Parente',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    filiation = Filiation.get_or_404(id)
    form = FiliationForm(request.form, obj=filiation)

    if form.validate() and request.method == 'PUT':
        form.populate_obj(filiation)
        filiation.update()
        return jsonify({'redirect': url_for('filiations.index')})

        return render_template('filiations/view.html',
                               form=form,
                               method='put',
                               label='Editar filho',
                               color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Filiation.get_or_404(id).delete()
    return '', 204
