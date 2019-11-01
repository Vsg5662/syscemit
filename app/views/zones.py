# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..extensions import excel
from ..forms.zones import ZoneForm, ZoneSearchForm
from ..models.zones import Zone

bp = Blueprint('zones', __name__, url_prefix='/regioes')


@bp.route('/')
@login_required
def index():
    form = ZoneSearchForm(request.args)
    grid = request.args.get('grid', 0, type=bool)
    export = request.args.get('export', 0, type=int)
    filters = form.filters.data
    criteria = form.criteria.data
    order = form.order.data
    pagination = Zone.fetch(filters, criteria, order, form.page.data)
    zones = pagination.items
    filters = {'filters-' + k: v for k, v in filters.items()}

    if export and current_user.is_admin():
        export = Zone.dump(pagination)
        return excel.make_response_from_array(export,
                                              'xlsx',
                                              file_name='Regiões.xlsx')

    if request.is_xhr and not grid:
        return jsonify({'result': [z.serialize() for z in zones]})

    return render_template('zones/index.html',
                           icon='fa-map-marked-alt',
                           title='Regiões',
                           clean_url=url_for('zones.index'),
                           create_url=url_for('zones.create'),
                           form=form,
                           filters=filters,
                           criteria=criteria,
                           order=order,
                           pagination=pagination,
                           zones=zones)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = ZoneForm()

    if form.validate() and request.method == 'POST':
        zone = Zone()
        form.populate_obj(zone)
        zone.save()
        return jsonify({'redirect': url_for('zones.index')})

    return render_template('zones/view.html',
                           icon='fa-map-marked-alt',
                           title='Adicionar Região',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit(id):
    view = request.args.get('format', '', type=str)
    view = True if not current_user.is_admin() else view
    title = 'Região' if view == 'view' else 'Editar Região'

    zone = Zone.get_or_404(id)
    obj = {'obj': zone} if request.method == 'GET' else {}
    form = ZoneForm(**obj)

    if form.validate() and current_user.is_admin() and request.method == 'PUT':
        form.populate_obj(zone)
        zone.update()
        return jsonify({'redirect': url_for('zones.index')})

    return render_template('zones/view.html',
                           icon='fa-map-marked-alt',
                           title=title,
                           form=form,
                           method='put',
                           color='warning',
                           view=bool(view))


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Zone.get_or_404(id).delete()
    return '', 204
