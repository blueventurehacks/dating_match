from flask import Blueprint, jsonify
from sqlalchemy import text
from ..models import db

health_bp = Blueprint('health', __name__, url_prefix='/health')

@health_bp.route('/db')
def health_db():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"db": "ok"})
    except Exception as exc:
        return jsonify({"db": "error", "detail": str(exc)}), 500
