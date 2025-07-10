from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Project, Transcript

projects_bp = Blueprint('projects', __name__)

# === Get all projects for the current user ===
@projects_bp.route('/api/projects', methods=['GET'])
@login_required
def get_projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return jsonify([p.to_dict() for p in projects]), 200

# === Create a new project ===
@projects_bp.route('/api/projects', methods=['POST'])
@login_required
def create_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({'error': 'Project name is required.'}), 400

    project = Project(name=name, description=description, user_id=current_user.id)
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201

# === Update project ===
@projects_bp.route('/api/projects/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    if not project:
        return jsonify({'error': 'Project not found.'}), 404

    project.name = name or project.name
    project.description = description
    db.session.commit()
    return jsonify(project.to_dict()), 200

# === Delete project ===
@projects_bp.route('/api/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    if not project:
        return jsonify({'error': 'Project not found.'}), 404

    # Optionally remove project assignment from transcripts
    Transcript.query.filter_by(project_id=project_id).update({'project_id': None})
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully.'}), 200

# === Get transcripts for a specific project ===
@projects_bp.route('/api/projects/<int:project_id>/transcripts', methods=['GET'])
@login_required
def get_project_transcripts(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    if not project:
        return jsonify({'error': 'Project not found or unauthorized'}), 404

    transcripts = Transcript.query.filter_by(project_id=project.id).all()
    return jsonify([
        {
            'id': t.id,
            'filename': t.filename,
            'status': t.status,
            'created_at': t.created_at.isoformat()
        } for t in transcripts
    ])
