# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, url_for
from flask_login import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    return redirect(url_for('deceased.index'))
