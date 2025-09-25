from flask import Blueprint, request, jsonify
from ..models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    payload = request.get_json(silent=True) or {}
    first_name = (payload.get("firstName") or "").strip()
    last_name = (payload.get("lastName") or "").strip()
    email_address = (payload.get("emailAddress") or "").strip().lower()
    password = payload.get("password") or ""

    if not first_name or not last_name or not email_address or not password:
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email_address=email_address).first():
        return jsonify({"message": "Email already registered"}), 409

    user = User(
        first_name=first_name,
        last_name=last_name,
        email_address=email_address,
        password_hash=User.hash_password(password),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    email_address = (payload.get("emailAddress") or "").strip().lower()
    password = payload.get("password") or ""

    if not email_address or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = User.query.filter_by(email_address=email_address).first()
    if not user or not user.verify_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify(user.to_dict()), 200
