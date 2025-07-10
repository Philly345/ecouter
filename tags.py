from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Tag, db

tags_bp = Blueprint('tags', __name__)

# === Get all tags for current user ===
@tags_bp.route('/api/tags', methods=['GET'])
@login_required
def get_tags():
    tags = Tag.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': t.id, 'name': t.name} for t in tags])

# === Create new tag ===
@tags_bp.route('/api/tags', methods=['POST'])
@login_required
def create_tag():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Tag name required'}), 400

    existing = Tag.query.filter_by(name=name.lower(), user_id=current_user.id).first()
    if existing:
        return jsonify({'error': 'Tag already exists'}), 409

    tag = Tag(name=name.lower(), user_id=current_user.id)
    db.session.add(tag)
    db.session.commit()

    return jsonify({'id': tag.id, 'name': tag.name}), 201

# === Delete a tag ===
@tags_bp.route('/api/tags/<int:tag_id>', methods=['DELETE'])
@login_required
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id, user_id=current_user.id).first()
    if not tag:
        return jsonify({'error': 'Tag not found'}), 404

    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Tag deleted'}), 200
