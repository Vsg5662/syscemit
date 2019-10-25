# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..forms.graves import COLUMNS, GraveForm, GraveSearchForm
from ..models.graves import Grave

bp = Blueprint('graves', __name__, url_prefix='/tumulos')


@bp.route('/')
@login_required
def index():
    form = GraveSearchForm(request.args)
    grid = request.args.get('grid', 0, type=bool)
    search = form.search.data
    criteria = form.criteria.data
    order = form.order.data
    pagination = Grave.fetch(search, criteria, order, form.page.data)
    graves = pagination.items

    if request.is_xhr and not grid:
        return jsonify({'result': [g.serialize() for g in graves]})

    return render_template('graves/index.html',
                           icon='fa-tombstone',
                           title='Túmulos',
                           clean_url=url_for('graves.index'),
                           create_url=url_for('graves.create'),
                           form=form,
                           search=search,
                           criteria=criteria,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           graves=graves)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = GraveForm()
    form.refill()

    if form.validate() and request.method == 'POST':
        grave = Grave()
        form.populate_obj(grave)
        grave.save()
        return jsonify({'redirect': url_for('graves.index')})

    return render_template('graves/view.html',
                           icon='fa-tombstone',
                           title='Adicionar Túmulo',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit(id):
    grave = Grave.get_or_404(id)
    form = GraveForm(request.form, obj=grave)
    view = request.args.get('format', '', type=str)
    title = 'Túmulo' if view == 'view' else 'Editar Túmulo'
    view = True if not current_user.is_admin() else view
    form.refill()

    if form.validate() and current_user.is_admin() and request.method == 'PUT':
        form.populate_obj(grave)
        grave.update()
        return jsonify({'redirect': url_for('graves.index')})

    return render_template('graves/view.html',
                           icon='fa-tombstone',
                           title=title,
                           form=form,
                           method='put',
                           color='warning',
                           view=bool(view))


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Grave.get_or_404(id).delete()
    return '', 204
