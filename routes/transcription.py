from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Transcript, Tag
from extensions import db
from werkzeug.utils import secure_filename
import os, datetime, json, time, requests, subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MYMEMORY_EMAIL = os.getenv("MYMEMORY_EMAIL", "phillyrick34@gmail.com")

client = OpenAI(api_key=OPENAI_API_KEY)
transcription_bp = Blueprint('transcription', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'webm', 'ogg', 'flac', 'mp4', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_audio_from_video(video_path, output_path):
    command = [
        'ffmpeg', '-i', video_path,
        '-vn', '-acodec', 'libmp3lame', '-q:a', '2',
        output_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def smart_paragraph_format(words, diarized):
    paragraphs = []
    current_paragraph = []
    last_end = 0
    last_speaker = None

    for word in words:
        start = word.get("start", 0) / 1000.0
        speaker = word.get("speaker", None) if diarized else None

        if (speaker and speaker != last_speaker) or (start - last_end > 1.2):
            if current_paragraph:
                paragraphs.append(" ".join([w["text"] for w in current_paragraph]))
                current_paragraph = []
        current_paragraph.append(word)
        last_end = word.get("end", 0) / 1000.0
        last_speaker = speaker

    if current_paragraph:
        paragraphs.append(" ".join([w["text"] for w in current_paragraph]))

    return "\n\n".join(paragraphs)

def translate_with_mymemory(text, target_lang="fr"):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"en|{target_lang}",
            "de": MYMEMORY_EMAIL
        }
        res = requests.get(url, params=params)
        data = res.json()
        return data["responseData"]["translatedText"]
    except Exception as e:
        print("❌ Translation error:", e)
        return None

@transcription_bp.route('/api/transcribe', methods=['POST'])
@login_required
def transcribe_audio():
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    verbatim = request.form.get('verbatim', 'true').lower() == 'true'
    diarization = request.form.get('diarization', 'false').lower() == 'true'
    target_language = request.form.get('language', 'en')

    try:
        original_filename = secure_filename(file.filename)
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(original_path)

        ext = original_filename.rsplit('.', 1)[1].lower()
        is_video = ext in ['mp4', 'mov']

        if is_video:
            audio_filename = original_filename.rsplit('.', 1)[0] + '.mp3'
            audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
            extract_audio_from_video(original_path, audio_path)
        else:
            audio_filename = original_filename
            audio_path = original_path

        transcript = Transcript(
            filename=original_filename,
            text='',
            summary='',
            word_timings=None,
            status='processing',
            user_id=current_user.id,
            created_at=datetime.datetime.utcnow()
        )

        project_id = request.form.get('project_id')
        if project_id:
            transcript.project_id = int(project_id)

        tags_input = request.form.get('tags')
        if tags_input:
            tag_names = [name.strip().lower() for name in tags_input.split(',') if name.strip()]
            for name in tag_names:
                existing_tag = Tag.query.filter_by(name=name, user_id=current_user.id).first()
                if not existing_tag:
                    existing_tag = Tag(name=name, user_id=current_user.id)
                    db.session.add(existing_tag)
                transcript.tags.append(existing_tag)

        db.session.add(transcript)
        db.session.commit()

        headers = {'authorization': ASSEMBLYAI_API_KEY}
        with open(audio_path, 'rb') as f:
            upload_res = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers=headers,
                files={'file': f}
            )
        upload_url = upload_res.json().get('upload_url')

        config = {
            "audio_url": upload_url,
            "speaker_labels": diarization,
            "language_code": target_language,
            "format_text": not verbatim,
            "punctuate": True
        }

        transcript_res = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers=headers,
            json=config
        )
        transcript_id = transcript_res.json().get('id')
        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

        while True:
            polling_res = requests.get(polling_endpoint, headers=headers)
            json_data = polling_res.json()
            if json_data['status'] == 'completed':
                break
            elif json_data['status'] == 'error':
                raise Exception(json_data.get("error", "Transcription failed"))
            time.sleep(3)

        words = json_data.get("words", [])
        utterances = json_data.get("utterances", [])

        if utterances:
            formatted = ""
            speaker_map = {}
            next_number = 1
            for utt in utterances:
                spk = utt.get("speaker", "Unknown")
                if spk not in speaker_map:
                    speaker_map[spk] = next_number
                    next_number += 1
                speaker_num = speaker_map[spk]
                formatted += f"Speaker {speaker_num}: {utt['text'].strip()}\n\n"
        else:
            formatted = smart_paragraph_format(words, diarization)

        if target_language != "en":
            translated_text = translate_with_mymemory(formatted, target_language)
            transcript.text = translated_text or formatted.strip()
        else:
            transcript.text = formatted.strip()

        transcript.word_timings = json.dumps(words)
        transcript.status = 'complete'
        db.session.commit()

        return jsonify({
            'transcript': transcript.text,
            'audio_url': f'{request.host_url}uploads/{audio_filename}',
            'word_timings': words
        }), 200

    except Exception as e:
        print("❌ Transcription error:", str(e))
        transcript.status = 'error'
        db.session.commit()
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@transcription_bp.route('/api/transcripts', methods=['GET'])
@login_required
def get_transcripts():
    try:
        transcripts = Transcript.query.filter_by(user_id=current_user.id).order_by(Transcript.created_at.desc()).all()
        results = []

        for t in transcripts:
            results.append({
                "id": t.id,
                "filename": t.filename,
                "text": t.text,
                "summary": t.summary,
                "status": t.status,
                "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "audio_url": f"{request.host_url}uploads/{t.filename}"
            })

        return jsonify(results), 200

    except Exception as e:
        print("❌ Failed to fetch transcripts:", e)
        return jsonify({"error": "Failed to load transcripts"}), 500

@transcription_bp.route('/api/transcripts/<int:transcript_id>', methods=['DELETE'])
@login_required
def delete_transcript(transcript_id):
    transcript = Transcript.query.get(transcript_id)

    if not transcript:
        return jsonify({'error': 'Transcript not found'}), 404

    if transcript.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        file_path = os.path.join(UPLOAD_FOLDER, transcript.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(transcript)
        db.session.commit()

        return jsonify({'message': 'Transcript deleted'}), 200

    except Exception as e:
        print("❌ Deletion error:", str(e))
        return jsonify({'error': 'Failed to delete transcript'}), 500

@transcription_bp.route('/api/transcripts/<int:transcript_id>', methods=['GET'])
@login_required
def get_single_transcript(transcript_id):
    try:
        transcript = Transcript.query.filter_by(id=transcript_id, user_id=current_user.id).first()
        if not transcript:
            return jsonify({'error': 'Transcript not found'}), 404

        return jsonify({
            "id": transcript.id,
            "filename": transcript.filename,
            "text": transcript.text,
            "summary": transcript.summary,
            "status": transcript.status,
            "created_at": transcript.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "project_id": transcript.project_id,
            "tags": [tag.name for tag in transcript.tags],
            "audio_url": f"{request.host_url}uploads/{transcript.filename}",
            "word_timings": json.loads(transcript.word_timings or "[]")
        }), 200

    except Exception as e:
        print("❌ Failed to fetch single transcript:", str(e))
        return jsonify({'error': 'Failed to load transcript'}), 500
