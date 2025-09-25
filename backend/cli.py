import click
from flask.cli import with_appcontext
from .models import db

def init_db_command(app):
    @app.cli.command("init-db")
    @with_appcontext
    def init_db():
        """Create tables if they do not exist."""
        db.create_all()
        print("Database initialized")
