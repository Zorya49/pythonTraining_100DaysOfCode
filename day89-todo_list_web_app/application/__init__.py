from flask import Flask
from .extensions import db, login_manager
from .routes import main
from .auth import auth
from .models import User, Task


def create_app(config_object='application.config.Config'):
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

        return app
