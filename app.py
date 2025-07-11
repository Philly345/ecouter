import os
from flask import Flask, jsonify, send_from_directory, current_app, request
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from flask_mail import Mail, Message
from flask_migrate import Migrate
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# === Import extensions ===
from extensions import db, login_manager, oauth, register_oauth_clients
from models import User

# === Initialize Flask app ===
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey')

# === Database configuration ===
db_path = os.path.join(app.instance_path, 'ecouter.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# === Email (Gmail SMTP) ===
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL')

# === Flask-Mail Init ===
mail = Mail(app)

# === Google OAuth ===
app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET")

# === OpenAI API ===
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Session & cookies ===
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

# === Init extensions ===
db.init_app(app)
login_manager.init_app(app)
oauth.init_app(app)
register_oauth_clients(app)
migrate = Migrate(app, db)

# === Enable CORS ===
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# === Login Manager Loader ===
@login_manager.user_loader
def load_user(user_id):
    with current_app.app_context():
        return db.session.get(User, int(user_id))

# === Ensure folders & DB ===
with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("avatars", exist_ok=True)

    if not os.path.exists(db_path):
        print("📦 Creating database...")
        open(db_path, 'a').close()
        db.create_all()
        print("✅ Database created.")
    else:
        try:
            db.create_all()
        except Exception as e:
            print("❌ Failed to apply schema:", e)

# === Send Email Function ===
def send_email(subject, recipient, body):
    try:
        msg = Message(subject=subject, recipients=[recipient], body=body)
        mail.send(msg)
        print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print("❌ Email sending error:", e)

# === Blueprints ===
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.transcription import transcription_bp
from routes.email import email_bp
from routes.translate import translate_bp
from routes.dashboard import dashboard_bp
from routes.projects import projects_bp
from routes.tags import tags_bp

# === Register Blueprints ===
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(transcription_bp)
app.register_blueprint(email_bp)
app.register_blueprint(translate_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(tags_bp)

# === Serve avatar files ===
@app.route('/avatars/<path:filename>')
def serve_avatar(filename):
    return send_from_directory('avatars', filename)

# === Serve uploaded audio ===
@app.route('/uploads/<path:filename>')
def serve_audio_file(filename):
    return send_from_directory('uploads', filename)

# === Debug session ===
@app.route('/debug-session')
def debug_session():
    return jsonify({
        "authenticated": current_user.is_authenticated,
        "user_id": current_user.get_id()
    })

# === Delete Transcript ===
@app.route('/api/delete/<int:transcript_id>', methods=['DELETE'])
@login_required
def delete_transcript(transcript_id):
    from models import Transcript
    transcript = Transcript.query.filter_by(id=transcript_id, user_id=current_user.id).first()
    if not transcript:
        return jsonify({'error': 'Transcript not found'}), 404

    db.session.delete(transcript)
    db.session.commit()
    return jsonify({'message': 'Transcript deleted successfully'}), 200

# === Notify when transcript is ready ===
@app.route('/api/notify_transcription_ready/<int:transcript_id>', methods=['POST'])
@login_required
def notify_transcription_ready(transcript_id):
    from models import Transcript
    transcript = Transcript.query.get(transcript_id)
    if not transcript or transcript.user_id != current_user.id:
        return jsonify({'error': 'Transcript not found or unauthorized'}), 404

    send_email(
        subject="Your Transcription is Ready",
        recipient=current_user.email,
        body=f"Hello {current_user.name},\n\nYour transcription '{transcript.filename}' is now ready!\n\nVisit the dashboard to view it.\n\n- Écouter Team"
    )
    return jsonify({'message': 'Notification sent successfully'}), 200

# === Test Email Endpoint ===
@app.route('/test-email')
def test_email():
    send_email(
        subject="Test Email from Écouter",
        recipient=os.getenv("SMTP_USERNAME"),
        body="✅ This is a test email from your Flask app using Gmail SMTP."
    )
    return jsonify({"message": "Test email sent!"})

# === AI Support Assistant Endpoint ===
@app.route('/api/support', methods=['POST'])
def support_chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "You are a support agent for Écouter.ai. Help users with transcription, login, account setup, etc."
                )},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response['choices'][0]['message']['content']})
    except Exception as e:
        print("❌ OpenAI error:", str(e))
        return jsonify({
            "reply": "Assistant is currently unavailable. Please email support."
        }), 200

# === Root route ===
@app.route('/')
def home():
    return jsonify({"message": "Écouter backend is running."})

# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
