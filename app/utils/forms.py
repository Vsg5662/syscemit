# -*- coding: utf-8 -*-

from wtforms import SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget

ORDERS = [('asc', 'Ascendente'), ('desc', 'Descente')]


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


def get_fields(form):
    return [(k, v) for k in form.__dict__.keys() if not k.startswith('_')
            for v in [getattr(form, k).args[0]]]
