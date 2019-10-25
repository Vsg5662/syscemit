# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from ..forms.auth import AuthLoginForm
from ..models.users import User

bp = Blueprint('auth', __name__, url_prefix='/conta')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = AuthLoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if form.validate() and request.method == 'POST':
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            data = {
                'redirect': request.args.get('next') or url_for('main.index')
            }
        else:
            data = {'redirect': request.url}
            flash('Usuário ou senha inválida', 'danger')
        return jsonify(data)

    return render_template('auth/login.html', form=form, method='post')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
