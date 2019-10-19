# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..forms.deceasedes import COLUMNS, DeceasedForm, DeceasedSearchForm
from ..models import Address, City, Deceased, Doctor, Grave, Registry, Zone

bp = Blueprint('deceasedes', __name__, url_prefix='/falecidos')


@bp.route('/')
@login_required
def index():
    form = DeceasedSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if filters_ and search:
        filters += tuple(
            getattr(Deceased, f).ilike('%' + search + '%') for f in filters_)
    elif search:
        filters += (Deceased.name.ilike('%' + search + '%'), )

    if order and clause:
        orders += (getattr(getattr(Deceased, clause), order)(), )

    if not orders:
        orders += (Deceased.name.asc(), )
    pagination = Deceased.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    deceasedes = pagination.items
    headers = [('name', 'Nome'), ('city', 'Cidade'),
               ('death_datetime', 'Data de Falecimento'), ('grave', 'Túmulo')]

    return render_template('deceasedes/index.html',
                           icon='fa-coffin',
                           title='Falecidos',
                           clean_url=url_for('deceasedes.index'),
                           create_url=url_for('deceasedes.create'),
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=headers,
                           deceasedes=deceasedes)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = DeceasedForm()
    form.gender.data = bool(form.gender.data)

    if form.birthplace_id.data:
        city = City.get_or_404(form.birthplace_id.data)
        form.birthplace_id.choices = [(city.id, f'{city.name} - {city.state.name}')]

    if form.home_address_id.data:
        address = Address.get_or_404(form.home_address_id.data)
        form.home_address_id.choices = [(
            address.id, f'{address.street} - {address.district}, {address.city.name} - {address.city.state.name}, {address.cep}')]

    if form.death_address_id.data:
        address = Address.get_or_404(form.death_address_id.data)
        form.death_address_id.choices = [(
            address.id, f'{address.street} - {address.district}, {address.city.name} - {address.city.state.name}, {address.cep}')]

    if form.doctor_id.data:
        doctor = Doctor.get_or_404(form.doctor_id.data)
        form.doctor_id.choices = [(doctor.id, f'{doctor.name} - {doctor.crm}')]

    if form.grave_id.data:
        grave = Grave.get_or_404(form.grave_id.data)
        form.grave_id.choices = [(grave.id, f'{grave.street} - {grave.number}, {grave.zone.description} - {grave.zone.complement}')]

    if form.registry_id.data:
        registry = Registry.get_or_404(form.registry_id.data)
        form.registry_id.choices = [(registry.id, f'{registry.name} - {registry.city.name}')]

    if form.validate() and request.method == 'POST':
        deceased = Deceased()
        form.populate_obj(deceased)
        deceased.save()
        return jsonify({'redirect': url_for('deceasedes.index')})

    print('#' * 100)
    print(form.errors)
    print('#' * 100)

    return render_template('deceasedes/view.html',
                           icon='fa-coffin',
                           title='Adicionar Falecido',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit(id):
    deceased = Deceased.get_or_404(id)
    form = DeceasedForm(request.form, obj=deceased)

    if form.birthplace_id.data:
        city = City.get_or_404(form.birthplace_id.data)
        form.birthplace_id.choices = [(city.id, f'{city.name} - {city.state.name}')]

    if form.home_address_id.data:
        address = Address.get_or_404(form.home_address_id.data)
        form.home_address_id.choices = [(
            address.id, f'{address.street} - {address.district}, {address.city.name} - {address.city.state.name}, {address.cep}')]

    if form.death_address_id.data:
        address = Address.get_or_404(form.home_death_id.data)
        form.death_address_id.choices = [(
            address.id, f'{address.street} - {address.district}, {address.city.name} - {address.city.state.name}, {address.cep}')]

    if form.doctor_id.data:
        doctor = Doctor.get_or_404(form.doctor_id.data)
        form.doctor_id.choices = [(doctor.id, f'{doctor.name} - {doctor.crm}')]

    if form.grave_id.data:
        grave = Grave.get_or_404(form.grave_id.data)
        form.grave_id.choices = [(grave.id, f'{grave.street} - {grave.number}, {grave.zone.description} - {grave.zone.complement}')]

    if form.registry_id.data:
        registry = Registry.get_or_404(form.registry_id.data)
        form.registry_id.choices = [(registry.id, f'{registry.name} - {registry.city.name}')]

    if request.args.get('format', '', type=str) == 'view':
        return render_template('deceasedes/view.html',
                               icon='fa-coffin',
                               title='Falecido',
                               form=form,
                               view=True)

    if form.validate() and current_user.is_admin and request.method == 'PUT':
        form.populate_obj(deceased)
        deceased.update()
        return jsonify({'redirect': url_for('deceasedes.index')})

    return render_template('deceasedes/view.html',
                           icon='fa-coffin',
                           title='Editar Falecido',
                           form=form,
                           method='put',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Deceased.get_or_404(id).delete()
    return '', 204
