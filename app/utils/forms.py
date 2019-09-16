# -*- coding: utf-8 -*-

from wtforms import SelectMultipleField, StringField
from wtforms.widgets import CheckboxInput, ListWidget, html5


class SearchField(StringField):
    widget = html5.SearchInput()


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()
