from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt
from app.models import User
from app.utils.validators import validate_email, validate_password, validate_username
from app.utils.decorators import logout_required

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Todos los campos son requeridos.', 'danger')
            return render_template('login.html')
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get('remember') == 'on')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        flash('Credenciales incorrectas.', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if not username or not email or not password or not confirm:
            flash('Todos los campos son requeridos.', 'danger')
            return render_template('register.html')
        if not validate_username(username):
            flash('Nombre de usuario inválido.', 'danger')
            return render_template('register.html')
        if not validate_email(email):
            flash('Correo electrónico inválido.', 'danger')
            return render_template('register.html')
        if password != confirm:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('register.html')
        if not validate_password(password):
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
            return render_template('register.html')
        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            flash('Usuario o correo ya registrado.', 'danger')
            return render_template('register.html')
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))