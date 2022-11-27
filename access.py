from functools import wraps
from flask import session, render_template, request, current_app


def login_required(func):
    @wraps(func)
    def wrapper(*argc, **kwargs):
        if 'user_id' in session:
            return func(*argc, **kwargs)
        return render_template('access_refused.html')
    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_func = request.endpoint   # Это имя блюпринт. имя обработчика
    print('endpoint_func', endpoint_func)
    endpoint_app = request.endpoint.split('.')[0]
    print('endpoint_app', endpoint_app)

    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and endpoint_app in config[user_group]:
            return True
        elif user_group in config and endpoint_func in config[user_group]:
            return True
    return False


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return "no access"
    return wrapper