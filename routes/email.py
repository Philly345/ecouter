from flask import Blueprint, request, jsonify
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from extensions import mail
from models import db, User
import os

email_bp = Blueprint('email', __name__)

# === Email Token Serializer ===
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except (SignatureExpired, BadSignature):
        return None
    return email

@email_bp.route('/verify-email')
def verify_email():
    token = request.args.get('token')
    if not token:
        return "Missing token ❌", 400

    email = confirm_token(token)
    if not email:
        return "Invalid or expired token ❌", 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return "User not found ❌", 404

    if user.is_verified:
        return "Account already verified ✅", 200

    user.is_verified = True
    db.session.commit()
    return "Email verified successfully! 🎉", 200

def send_verification_email(email, token):
    verify_url = f"http://localhost:5000/verify-email?token={token}"
    msg = Message("Verify Your Email", recipients=[email])
    msg.body = f"Click the link to verify your email: {verify_url}"
    mail.send(msg)
