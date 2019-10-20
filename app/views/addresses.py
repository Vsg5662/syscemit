# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..forms.addresses import COLUMNS, AddressForm, AddressSearchForm
from ..models import Address, City

bp = Blueprint('addresses', __name__, url_prefix='/enderecos')


@bp.route('/')
@login_required
def index():
    form = AddressSearchForm(request.args)
    grid = request.args.get('grid', 0, type=bool)
    search = form.search.data
    criteria = form.criteria.data
    order = form.order.data

    pagination = Address.fetch(search, criteria, order, form.page.data)
    addresses = pagination.items

    if request.is_xhr and not grid:
        return jsonify({
            'result': [{
                'id':
                a.id,
                'name': (f'{a.street} - {a.district},'
                         ' {a.city.name} - {a.city.state.name}, {a.cep}')
            } for a in addresses]
        })

    return render_template('addresses/index.html',
                           icon='fa-map-signs',
                           title='Endereços',
                           clean_url=url_for('addresses.index'),
                           create_url=url_for('addresses.create'),
                           form=form,
                           search=search,
                           criteria=criteria,
                           order=order,
                           pagination=pagination,
                           headers=COLUMNS,
                           addresses=addresses)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = AddressForm()

    if form.city_id.data:
        city = City.get_or_404(form.city_id.data)
        form.city_id.choices = [(city.id, f'{city.name} - {city.state.name}')]

    if form.validate() and request.method == 'POST':
        address = Address()
        form.populate_obj(address)
        address.save()
        return jsonify({'redirect': url_for('addresses.index')})

    return render_template('addresses/view.html',
                           icon='fa-map-signs',
                           title='Adicionar Endereço',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
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

    if form.validate() and current_user.is_admin and request.method == 'PUT':
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
