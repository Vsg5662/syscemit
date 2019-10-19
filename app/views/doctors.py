# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.doctors import COLUMNS, DoctorForm, DoctorSearchForm
from ..models import Doctor

bp = Blueprint('doctors', __name__, url_prefix='/medicos')


@bp.route('/')
@login_required
def index():
    form = DoctorSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if filters_ and search:
        filters += tuple(
            getattr(Doctor, f).ilike('%' + search + '%') for f in filters_)
    elif search:
        filters += (Doctor.name.ilike('%' + search + '%'), )

    if order and clause:
        orders += (getattr(getattr(Doctor, clause), order)(), )

    if not orders:
        orders += (Doctor.name.asc(), )
    pagination = Doctor.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    doctors = pagination.items

    return render_template('doctors/index.html',
                           icon='fa-user-md',
                           title='Médicos',
                           clean_url=url_for('addresses.index'),
                           create_url=url_for('addresses.create'),
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           doctors=doctors)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = DoctorForm()

    if form.validate() and request.method == 'POST':
        doctor = Doctor()
        form.populate_obj(doctor)
        doctor.save()
        return jsonify({'redirect': url_for('doctors.index')})

    return render_template('doctors/view.html',
                           icon='fa-user-md',
                           title='Adicionar Médico',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit(id):
    doctor = Doctor.get_or_404(id)
    form = DoctorForm(request.form, obj=doctor)

    if request.args.get('format', '', type=str) == 'view':
        return render_template('doctors/view.html',
                               icon='fa-user-md',
                               title='Médico',
                               form=form,
                               view=True)

    if form.validate() and current_user.is_admin and request.method == 'PUT':
        form.populate_obj(doctor)
        doctor.update()
        return jsonify({'redirect': url_for('doctors.index')})

    return render_template('doctors/view.html',
                           icon='fa-user-md',
                           title='Editar Médico',
                           form=form,
                           method='put',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Doctor.get_or_404(id).delete()
    return '', 204
