from flask import Flask
from config import Config
from extensions import db, cors
from models import User
from routes.auth import auth_bp
from routes.health import health_bp
from cli import init_db_command

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    cors(app, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)

    # Register CLI commands
    init_db_command(app)

    return app

app = create_app()

