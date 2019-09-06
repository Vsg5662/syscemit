# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import login_required, login_user, logout_user

from ..decorators import permission_required
from ..forms.users import UserForm, UserLoginForm
from ..models import User

bp = Blueprint('users', __name__, url_prefix='/usuarios')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Usuário ou senha inválida')
    return render_template('users/login.html', form=form)


@bp.route('/redefinir_senha', methods=['GET', 'POST'])
@login_required
def reset():
    return 'Pão de batata'


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    page = request.args.get('pagina', 1, type=int)
    pagination = User.query.paginate(page,
                                     per_page=current_app.config['PER_PAGE'],
                                     error_out=False)
    users = pagination.items
    return render_template('users/index.html',
                           pagination=pagination,
                           users=users)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = UserForm()
    return render_template('users/view.html',
                           form=form,
                           label='Adicionar Usuário',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'UPDATE'])
@login_required
@permission_required('admin')
def edit(id):
    user = User.get_or_404(id)
    form = UserForm(request.form, obj=user)
    return render_template('users/view.html',
                           form=form,
                           label='Editar Usuário',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    User.get_or_404(id).delete()
    return '', 204
