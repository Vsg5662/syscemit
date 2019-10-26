# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..forms.addresses import AddressForm, AddressSearchForm
from ..models.addresses import Address

bp = Blueprint('addresses', __name__, url_prefix='/enderecos')


@bp.route('/')
@login_required
def index():
    form = AddressSearchForm(request.args)
    grid = request.args.get('grid', 0, type=bool)
    filters = form.filters.data
    criteria = form.criteria.data
    order = form.order.data
    pagination = Address.fetch(filters, criteria, order, form.page.data)
    addresses = pagination.items

    if request.is_xhr and not grid:
        return jsonify({'result': [a.serialize() for a in addresses]})

    filters = {'filters-' + k: v for k, v in filters.items()}
    return render_template('addresses/index.html',
                           icon='fa-map-signs',
                           title='Endereços',
                           clean_url=url_for('addresses.index'),
                           create_url=url_for('addresses.create'),
                           form=form,
                           filters=filters,
                           criteria=criteria,
                           order=order,
                           pagination=pagination,
                           addresses=addresses)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = AddressForm()
    form.refill()

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
    view = request.args.get('format', '', type=str)
    view = True if not current_user.is_admin() else view
    title = 'Endereço' if view == 'view' else 'Editar Endereço'
    form.refill()

    if form.validate() and current_user.is_admin() and request.method == 'PUT':
        form.populate_obj(address)
        address.update()
        return jsonify({'redirect': url_for('addresses.index')})

    return render_template('addresses/view.html',
                           icon='fa-map-signs',
                           title=title,
                           form=form,
                           method='put',
                           color='warning',
                           view=bool(view))


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Address.get_or_404(id).delete()
    return '', 204
