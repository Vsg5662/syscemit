# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.childrens import COLUMNS, ChildrenForm, ChildrenSearchForm
from ..models import Children

bp = Blueprint('childrens', __name__, url_prefix='/filiacao')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = ChildrenSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if filters_ and search:
        filters += tuple(
            getattr(Children, f).ilike('%' + search + '%') for f in filters_)
    elif search:
        filters += (Children.name.ilike('%' + search + '%'), )

    if order and clause:
        orders += (getattr(getattr(Children, clause), order)(), )

    if not orders:
        orders += (Children.name.asc(), )
    pagination = Children.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    childrens = pagination.items

    return render_template('childrens/index.html',
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           childrens=childrens)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = ChildrenForm()
    if form.validate():
        children = Children()
        form.populate_obj(children)
        children.save()
        return jsonify({'redirect': url_for('childrens.index')})
    return render_template('childrens/view.html',
                           form=form,
                           method='post',
                           label='Adicionar filho',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    children = Children.get_or_404(id)
    form = ChildrenForm(request.form, obj=children)
    if form.validate():
        form.populate_obj(children)
        children.update()
        return jsonify({'redirect': url_for('childrens.index')})
    return render_template('childrens/view.html',
                           form=form,
                           method='put',
                           label='Editar filho',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Children.get_or_404(id).delete()
    return '', 204
