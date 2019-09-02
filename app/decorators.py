# -*- coding: utf-8 -*-

from functools import wraps

from flask import abort
from flask_login import current_user


def permission_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if (current_user.is_authenticated
                and current_user.has_permissions(*roles)):
                return f(*args, **kwargs)
            return abort(403)
        return wrapped
    return decorator
