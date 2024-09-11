from flask import Flask, session
from flask_bootstrap import Bootstrap5
from .extensions import db, login_manager
from .routes import main
from .auth import auth
from .models import User, Product, Order


def create_app(config_object='app.config.Config'):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

        app.register_blueprint(main)
        app.register_blueprint(auth)

        Bootstrap5(app)
        return app
