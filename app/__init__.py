from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig
from app.extensions import db, migrate, login_manager, bcrypt, cors
import os

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        env = os.environ.get('FLASK_ENV', 'development')
        if env == 'production':
            app.config.from_object(ProductionConfig)
        elif env == 'testing':
            app.config.from_object(TestingConfig)
        else:
            app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder.'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.marketplace import marketplace_bp
    from app.routes.aveologia import aveologia_bp
    from app.routes.calculadora import calculadora_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
    app.register_blueprint(aveologia_bp, url_prefix='/aveologia')
    app.register_blueprint(calculadora_bp, url_prefix='/calculadora')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app