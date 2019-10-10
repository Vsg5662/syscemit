# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import login_required, login_user, logout_user

from ..forms.auth import AuthLoginForm
from ..models import User

bp = Blueprint('auth', __name__, url_prefix='/conta')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = AuthLoginForm()
    if form.validate():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return jsonify({
                'redirect':
                request.args.get('next') or url_for('main.index')
            })
        flash('Usuário ou senha inválida')
    return render_template('auth/login.html', form=form, method='post')


@bp.route('/redefinir_senha', methods=['GET', 'POST'])
@login_required
def reset():
    return 'Pão de batata'


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
