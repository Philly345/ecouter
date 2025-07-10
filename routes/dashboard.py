from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import Transcript
from extensions import db
from sqlalchemy import func
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    try:
        # User data
        user_data = {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "verified": current_user.verified,
            "country": current_user.country,
            "gender": current_user.gender,
            "joined": current_user.created_at.strftime('%Y-%m-%d') if current_user.created_at else None,
            "avatar": current_user.avatar
        }

        # Transcripts data
        transcripts = Transcript.query.filter_by(user_id=current_user.id).order_by(Transcript.created_at.desc()).all()
        transcript_list = [
            {
                "id": t.id,
                "filename": t.filename,
                "text": t.text,
                "summary": t.summary,
                "created_at": t.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for t in transcripts
        ]

        total_transcripts = len(transcripts)

        # Language counts
        language_counts = db.session.query(
            Transcript.language, func.count(Transcript.id)
        ).filter_by(user_id=current_user.id).group_by(Transcript.language).all()

        language_usage = {
            lang or "Unknown": count for lang, count in language_counts
        }

        return jsonify({
            "user": user_data,
            "transcripts": transcript_list,
            "analytics": {
                "total_transcripts": total_transcripts,
                "language_usage": language_usage
            }
        }), 200

    except Exception as e:
        print("❌ Dashboard error:", str(e))
        return jsonify({"error": "Failed to load dashboard data"}), 500
