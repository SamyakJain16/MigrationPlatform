from flask import Flask
from .config import Config
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Set up JWT
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    jwt = JWTManager(app)  # Initialize the JWT manager

    # Register blueprints for different features
    from .auth import auth_bp
    from .agents import agents_bp
    from .documents import documents_bp
    from .status import status_bp
    from .dashboard import dashboard_bp
    from .routes import main_bp  # Import the routes blueprint

    app.register_blueprint(auth_bp)
    app.register_blueprint(agents_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)  # Register the main blueprint

    return app
