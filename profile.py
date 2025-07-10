from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        "userId": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "country": current_user.country or '',
        "gender": current_user.gender or '',
        "age": current_user.age or '',
        "age_change_count": current_user.age_change_count or 0,
        "provider": current_user.provider,
        "name_change_count": current_user.name_change_count or 0
    })


@profile_bp.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    name = request.form.get('name', '').strip()
    country = request.form.get('country', '').strip()
    gender = request.form.get('gender', '').strip()
    age = request.form.get('age', '').strip()  # Expecting "YYYY-MM-DD"

    if not name:
        return jsonify({'error': 'Name cannot be empty'}), 400

    # --- Name Editing Rules ---
    if current_user.provider == 'google':
        if name != current_user.name:
            if current_user.name_change_count >= 2:
                return jsonify({'error': 'Name change limit reached'}), 403
            current_user.name = name
            current_user.name_change_count += 1
    else:
        current_user.name = name

    # --- Age (birthdate) change limit (max 2 times) ---
    if age:
        if age != str(current_user.age):
            if current_user.age_change_count >= 2:
                return jsonify({'error': 'Age change limit reached'}), 403
            try:
                # Validate date format
                datetime.strptime(age, "%Y-%m-%d")
                current_user.age = age
                current_user.age_change_count += 1
            except ValueError:
                return jsonify({'error': 'Invalid date format (YYYY-MM-DD)'}), 400

    # --- Other fields ---
    current_user.country = country
    current_user.gender = gender

    try:
        db.session.add(current_user)
        db.session.commit()
        db.session.refresh(current_user)
        return jsonify({'message': 'Profile updated successfully'})
    except Exception as e:
        db.session.rollback()
        print("❌ Failed to update profile:", e)
        return jsonify({'error': 'Failed to update profile'}), 500
