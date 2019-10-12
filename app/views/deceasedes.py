# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.deceasedes import COLUMNS, DeceasedForm, DeceasedSearchForm
from ..models import Deceased

bp = Blueprint('deceasedes', __name__, url_prefix='/falecidos')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = DeceasedSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if filters_ and search:
        filters += tuple(
            getattr(Deceased, f).ilike('%' + search + '%') for f in filters_)
    elif search:
        filters += (Deceased.name.ilike('%' + search + '%'), )

    if order and clause:
        orders += (getattr(getattr(Deceased, clause), order)(), )

    if not orders:
        orders += (Deceased.name.asc(), )
    pagination = Deceased.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    deceasedes = pagination.items

    return render_template('deceasedes/index.html',
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           deceasedes=deceasedes)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = DeceasedForm()
    if form.validate():
        deceased = Deceased()
        form.populate_obj(deceased)
        deceased.save()
        return jsonify({'redirect': url_for('deceasedes.index')})
    return render_template('deceasedes/view.html',
                           form=form,
                           method='post',
                           label='Adicionar Falecido',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    deceased = Deceased.get_or_404(id)
    form = DeceasedForm(request.form, obj=deceased)
    if form.validate():
        form.populate_obj(deceased)
        deceased.update()
        return jsonify({'redirect': url_for('deceasedes.index')})
    return render_template('deceasedes/view.html',
                           form=form,
                           method='put',
                           label='Editar Falecido',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Deceased.get_or_404(id).delete()
    return '', 204
