# -*- coding: utf-8 -*-


def strftime(value, format='%d/%m/%Y %H:%M'):
    '''Format a date time to (Default): d Mon YYYY HH:MM P'''
    if value is None:
        return ''
    return value.strftime(format)
