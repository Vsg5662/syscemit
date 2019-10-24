# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname('__file__'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'KTpSJi2F8Ry!wxOnzw7{f1ON0Qdvq@yG'
    PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Development(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'storage-dev.db')
    SQLALCHEMY_ECHO = True


class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'storage.db')


config = {'development': Development, 'production': Production}
