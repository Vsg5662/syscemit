#!/usr/bin/env python3

import os

from app import create_app
from config import config

app = create_app(config=config[os.environ.get('FLASK_ENV', 'development')])

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=80)
