# -*- coding: utf-8 -*-

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)
from flask_login import current_user, login_required

from ..decorators import permission_required
from ..forms.addresses import AddressForm
from ..forms.deceasedes import COLUMNS, DeceasedForm, DeceasedSearchForm
from ..models import Deceased

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
    home_address_form = AddressForm()
    death_address_form = AddressForm()

    if form.validate() and request.method == 'POST':
        deceased = Deceased()
        form.populate_obj(deceased)
        deceased.save()
        return jsonify({'redirect': url_for('deceasedes.index')})

    return render_template('deceasedes/view.html',
                           icon='fa-coffin',
                           title='Adicionar Falecido',
                           form=form,
                           home_address_form=home_address_form,
                           death_address_form=death_address_form,
                           method='post',
                           color='success')


@bp.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit(id):
    deceased = Deceased.get_or_404(id)
    form = DeceasedForm(request.form, obj=deceased)

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
