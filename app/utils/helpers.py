# -*- coding: utf-8 -*-

from flask import jsonify, render_template


def shell_context(app, db, *models):
    '''
    Creates a shell context wrapper to flask cli

    :param app: application object
    :param db: database ORM instance
    :param models: list of model objects
    '''
    models = dict((m.__name__, m) for m in models)
    return dict(app=app, db=db, **models)


class HandleError():
    '''
    Create error pages for flask

    :param template: template to render on error page.
    :param message: error message to be showed.
    '''
    def __init__(self, template, message):
        self.message = message
        self.template = template

    def __call__(self, error):
        '''
        :param error: Error object of errorhandler
        '''
        return render_template(self.template, error=self.message), error.code


class HandleAPIError():
    '''
    Create error pages for flask jsonify

    :param message: error message to be showed.
    '''
    def __init__(self, message):
        self.message = message

    def __call__(self, error):
        '''
        :param error: Error object of errorhandler
        '''
        return jsonify(message=self.message, status=error.code), error.code
