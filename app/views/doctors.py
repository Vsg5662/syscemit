# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..forms.doctors import COLUMNS, DoctorForm, DoctorSearchForm
from ..models.doctors import Doctor

bp = Blueprint('doctors', __name__, url_prefix='/medicos')


@bp.route('/')
@login_required
def index():
    form = DoctorSearchForm(request.args)
    grid = request.args.get('grid', 0, type=bool)
    search = form.search.data
    criteria = form.criteria.data
    order = form.order.data
    pagination = Doctor.fetch(search, criteria, order, form.page.data)
    doctors = pagination.items

    if request.is_xhr and not grid:
        return jsonify({'result': [d.serialize() for d in doctors]})

    return render_template('doctors/index.html',
                           icon='fa-user-md',
                           title='Médicos',
                           clean_url=url_for('doctors.index'),
                           create_url=url_for('doctors.create'),
                           form=form,
                           search=search,
                           criteria=criteria,
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
    view = request.args.get('format', '', type=str)
    title = 'Médico' if view == 'view' else 'Editar Médico'

    if form.validate() and current_user.is_admin and request.method == 'PUT':
        form.populate_obj(doctor)
        doctor.update()
        return jsonify({'redirect': url_for('doctors.index')})

    return render_template('doctors/view.html',
                           icon='fa-user-md',
                           title=title,
                           form=form,
                           method='put',
                           color='warning',
                           view=bool(view))


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Doctor.get_or_404(id).delete()
    return '', 204
