#!/usr/bin/env python3

import os

from app import create_app
from config import config

app = create_app(config=config[os.environ.get('FLASK_ENV', 'development')])
