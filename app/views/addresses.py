# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import login_required

from ..decorators import permission_required
from ..forms.addresses import COLUMNS, AddressForm, AddressSearchForm
from ..models import Address, City

bp = Blueprint('addresses', __name__, url_prefix='/enderecos')


@bp.route('/')
@login_required
@permission_required('admin')
def index():
    form = AddressSearchForm(request.args)
    joins = filters = orders = ()
    search = form.search.data
    filters_ = form.filters.data
    clause = form.clause.data
    order = form.order.data

    if 'city' in filters or clause == 'city':
        joins += (City, )

    if filters_ and search:
        filters += tuple(
            getattr(Address, f).ilike('%' + search + '%') for f in filters_
            if f != 'city')
        if 'city' in filters_:
            filters += (
                Address.city_id == City.id,
                City.name.ilike('%' + search + '%'),
            )
    elif search:
        filters += (Address.street.ilike('%' + search + '%'), )

    if order and clause:
        if clause != 'city':
            orders += (getattr(getattr(Address, clause), order)(), )
        else:
            orders += (getattr(City.name, order)(), )

    if not orders:
        orders += (Address.street.asc(), )
    pagination = Address.query.join(*joins).filter(*filters).order_by(
        *orders).paginate(form.page.data,
                          per_page=current_app.config['PER_PAGE'],
                          error_out=False)
    addresses = pagination.items

    if request.is_xhr:
        return jsonify({
            'result': [{
                'id': a.id,
                'name': f'{a.street} - {a.district}, {a.city.name} - {a.city.state.name}, {a.cep}'
            } for a in addresses]
        })
    return render_template('addresses/index.html',
                           icon='fa-map-signs',
                           title='Endereços',
                           clean_url=url_for('addresses.index'),
                           create_url=url_for('addresses.create'),
                           form=form,
                           search=search,
                           filters=filters_,
                           clause=clause,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           addresses=addresses)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = AddressForm()
    modal = request.args.get('modal', 0, type=bool)

    if form.city_id.data:
        city = City.get_or_404(form.city_id.data)
        form.city_id.choices = [(city.id, f'{city.name} - {city.state.name}')]

    if form.validate() and request.method == 'POST':
        address = Address()
        form.populate_obj(address)
        address.save()
        if modal:
            return jsonify({})
        return jsonify({'redirect': url_for('addresses.index')})
    return render_template('addresses/view.html',
                           icon='fa-map-signs',
                           title='Adicionar Endereço',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
@permission_required('admin')
def edit(id):
    address = Address.get_or_404(id)
    form = AddressForm(request.form, obj=address)

    if form.city_id.data:
        city = City.get_or_404(form.city_id.data)
        form.city_id.choices = [(city.id, f'{city.name} - {city.state.name}')]

    if request.args.get('format', '', type=str) == 'view':
        return render_template('addresses/view.html',
                               icon='fa-map-signs',
                               title='Endereço',
                               form=form,
                               view=True)

    if form.validate() and request.method == 'PUT':
        form.populate_obj(address)
        address.update()
        return jsonify({'redirect': url_for('addresses.index')})
    return render_template('addresses/view.html',
                           icon='fa-map-signs',
                           title='Editar Endereço',
                           form=form,
                           method='put',
                           color='warning')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Address.get_or_404(id).delete()
    return '', 204
