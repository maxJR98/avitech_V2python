from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            flash('Por favor inicia sesión.', 'warning')
            return redirect(url_for('auth.login'))
            
        if current_user.id_rol not in [1, 3]:
            flash('No tienes permisos de administrador.', 'danger')
            return redirect(url_for('main.index'))
            
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('Ya has iniciado sesión.', 'info')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function