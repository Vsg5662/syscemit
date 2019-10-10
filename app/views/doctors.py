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
@permission_required('admin')
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
        if clause != 'type':
            orders += (getattr(getattr(Doctor, clause), order)(), )
        else:
            orders += (getattr(DoctorType.description, order)(), )

    if not orders:
        orders += (Doctor.name.asc(), )
    pagination = Doctor.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    doctors = pagination.items

    return render_template('doctors/index.html',
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
    if form.validate():
        doctor = Doctor()
        form.populate_obj(doctor)
        doctor.save()
        return jsonify({'redirect': url_for('doctors.index')})
    return render_template('doctors/view.html',
                           form=form,
                           method='post',
                           label='Adicionar Médico',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    doctor = Doctor.get_or_404(id)
    form = DoctorForm(request.form, obj=doctor)
    if form.validate():
        form.populate_obj(doctor)
        doctor.update()
        return jsonify({'redirect': url_for('doctors.index')})
    return render_template('doctors/view.html',
                           form=form,
                           method='put',
                           label='Editar Médico',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Doctor.get_or_404(id).delete()
    return '', 204
