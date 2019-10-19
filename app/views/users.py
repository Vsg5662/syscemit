# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.users import COLUMNS, UserForm, UserSearchForm
from ..models import User, UserType

bp = Blueprint('users', __name__, url_prefix='/usuarios')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = UserSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if 'type' in filters or clause == 'type':
        joins += (UserType, )

    if filters_ and search:
        filters += tuple(
            getattr(User, f).ilike('%' + search + '%') for f in filters_
            if f != 'type')
        if 'type' in filters_:
            filters += (
                User.user_type_id == UserType.id,
                UserType.description.ilike('%' + search + '%'),
            )
    elif search:
        filters += (User.name.ilike('%' + search + '%'), )

    if order and clause:
        if clause != 'type':
            orders += (getattr(getattr(User, clause), order)(), )
        else:
            orders += (getattr(UserType.description, order)(), )

    if not orders:
        orders += (User.name.asc(), )
    pagination = User.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    users = pagination.items

    return render_template('users/index.html',
                           icon='fa-users',
                           title='Usuários',
                           clean_url=url_for('users.index'),
                           create_url=url_for('users.create'),
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
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
    user = User.get_or_404(id)
    form = UserForm(request.form, obj=user)

    if request.args.get('format', '', type=str) == 'view':
        return render_template('users/view.html',
                               icon='fa-users',
                               title='Usuário',
                               form=form,
                               view=True)

    if form.validate() and request.method == 'PUT':
        form.populate_obj(user)
        user.update()
        return jsonify({'redirect': url_for('users.index')})

    return render_template('users/view.html',
                           icon='fa-users',
                           title='Editar Usuário',
                           form=form,
                           method='put',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    User.get_or_404(id).delete()
    return '', 204
