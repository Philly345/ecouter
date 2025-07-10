from flask import Blueprint, request, jsonify, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from extensions import oauth, db
from models import User
import uuid
import secrets

# Email verification utilities
from routes.email import generate_confirmation_token, send_verification_email

auth_bp = Blueprint('auth', __name__)

# === Signup with email/password ===
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    hashed_pw = generate_password_hash(password)
    user = User(
        generated_id=str(uuid.uuid4()),
        email=email,
        name=name,
        password=hashed_pw,
        verified=False,
        provider='local'
    )
    db.session.add(user)
    db.session.commit()

    token = generate_confirmation_token(email)
    send_verification_email(email, token)

    return jsonify({'message': 'Account created! Please check your email to verify.'}), 201


# === Google OAuth Login Start ===
@auth_bp.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_callback', _external=True)
    nonce = secrets.token_urlsafe(16)
    session['google_oauth_nonce'] = nonce
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)


# === Google OAuth Callback ===
@auth_bp.route('/login/google/callback')
def google_callback():
    try:
        token = oauth.google.authorize_access_token()
        resp = oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo')
        user_info = resp.json()
    except Exception as e:
        return jsonify({'error': f'Google login failed: {str(e)}'}), 400

    if not user_info:
        return jsonify({'error': 'Failed to fetch user info from Google'}), 400

    email = user_info.get('email')
    name = user_info.get('name')
    avatar_url = user_info.get('picture')
    google_id = user_info.get('sub')

    if not email:
        return jsonify({'error': 'Google account has no email'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        # ✅ First-time Google user
        user = User(
            generated_id=str(uuid.uuid4()),
            email=email,
            name=name,
            verified=True,
            provider='google',
            avatar=avatar_url
        )
        db.session.add(user)
        db.session.commit()
        session['first_login'] = True
    else:
        session['first_login'] = False

    login_user(user)
    return redirect('http://localhost:3000/post-login')


# === Session Info (used by frontend PostLogin.js) ===
@auth_bp.route('/api/session')
def session_info():
    if current_user.is_authenticated:
        first_login = session.pop('first_login', False)
        return jsonify({
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "first_login": first_login
        }), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401


# === Logout ===
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
