# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import login_required

from ..decorators import permission_required
from ..extensions import excel
from ..forms.users import UserForm, UserSearchForm
from ..models.users import User

bp = Blueprint('users', __name__, url_prefix='/usuarios')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = UserSearchForm(request.args)
    export = request.args.get('export', 0, type=int)
    filters = form.filters.data
    criteria = form.criteria.data
    order = form.order.data
    pagination = User.fetch(filters, criteria, order, form.page.data)
    users = pagination.items
    filters = {'filters-' + k: v for k, v in filters.items()}

    if export:
        export = User.dump(pagination)
        return excel.make_response_from_array(export,
                                              'xlsx',
                                              file_name='Usuários.xlsx')

    return render_template('users/index.html',
                           icon='fa-users',
                           title='Usuários',
                           clean_url=url_for('users.index'),
                           create_url=url_for('users.create'),
                           form=form,
                           filters=filters,
                           criteria=criteria,
                           order=order,
                           pagination=pagination,
                           users=users)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = UserForm()

    if form.validate() and request.method == 'POST':
        user = User()
        form.populate_obj(user)
        user.save()
        return jsonify({'redirect': url_for('users.index')})

    return render_template('users/view.html',
                           icon='fa-users',
                           title='Adicionar Usuário',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    view = request.args.get('format', '', type=str)
    title = 'Usuário' if view == 'view' else 'Editar Usuário'

    user = User.get_or_404(id)
    obj = {'obj': user} if request.method == 'GET' else {}
    form = UserForm(**obj)

    if form.validate() and request.method == 'PUT':
        form.populate_obj(user)
        user.update()
        return jsonify({'redirect': url_for('users.index')})

    return render_template('users/view.html',
                           icon='fa-users',
                           title=title,
                           form=form,
                           method='put',
                           color='warning',
                           view=bool(view))


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    User.get_or_404(id).delete()
    return '', 204
