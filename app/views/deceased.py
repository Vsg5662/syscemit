# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..extensions import excel
from ..forms.deceased import DeceasedForm, DeceasedSearchForm
from ..models.deceased import Deceased

bp = Blueprint('deceased', __name__, url_prefix='/falecidos')


@bp.route('/')
@login_required
def index():
    form = DeceasedSearchForm(request.args)
    export = request.args.get('export', 0, type=int)
    filters = form.filters.data
    criteria = form.criteria.data
    order = form.order.data
    pagination = Deceased.fetch(filters, criteria, order, form.page.data)
    deceased = pagination.items
    filters = {'filters-' + k: v for k, v in filters.items()}

    if export and current_user.is_admin():
        export = Deceased.dump(pagination)
        return excel.make_response_from_array(export,
                                              'xlsx',
                                              file_name='Falecidos.xlsx')

    return render_template('deceased/index.html',
                           icon='fa-coffin',
                           title='Falecidos',
                           clean_url=url_for('deceased.index'),
                           create_url=url_for('deceased.create'),
                           form=form,
                           filters=filters,
                           criteria=criteria,
                           order=order,
                           pagination=pagination,
                           deceased=deceased)


@bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def create():
    form = DeceasedForm()
    form.refill()

    if form.validate() and request.method == 'POST':
        deceased = Deceased()
        form.populate_obj(deceased)
        deceased.save()
        return jsonify({'redirect': url_for('deceased.index')})

    return render_template('deceased/view.html',
                           icon='fa-coffin',
                           title='Adicionar Falecido',
                           form=form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit(id):
    view = request.args.get('format', '', type=str)
    view = True if not current_user.is_admin() else view
    title = 'Falecido' if view == 'view' else 'Editar Falecido'

    deceased = Deceased.get_or_404(id)
    obj = {'obj': deceased} if request.method == 'GET' else {}
    form = DeceasedForm(**obj)
    form.refill()

    if form.validate() and current_user.is_admin() and request.method == 'PUT':
        form.populate_obj(deceased)
        deceased.update()
        return jsonify({'redirect': url_for('deceased.index')})
    print('-' * 50)
    print(form.data)
    print(form.errors)
    print('-' * 50)

    return render_template('deceased/view.html',
                           icon='fa-coffin',
                           title=title,
                           form=form,
                           method='put',
                           color='warning',
                           view=bool(view))


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@permission_required('admin')
def delete(id):
    Deceased.get_or_404(id).delete()
    return '', 204
