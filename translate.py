from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Transcript
from extensions import db
import requests

translate_bp = Blueprint('translate', __name__)

MYMEMORY_API_KEY = "ffed8327de45e600ae43"

# Full language mapping: common language names → ISO-639-1 codes
LANGUAGE_MAP = {
    "afrikaans": "af", "albanian": "sq", "amharic": "am", "arabic": "ar",
    "armenian": "hy", "azerbaijani": "az", "basque": "eu", "belarusian": "be",
    "bengali": "bn", "bosnian": "bs", "bulgarian": "bg", "catalan": "ca",
    "cebuano": "ceb", "chichewa": "ny", "chinese": "zh", "corsican": "co",
    "croatian": "hr", "czech": "cs", "danish": "da", "dutch": "nl",
    "english": "en", "esperanto": "eo", "estonian": "et", "filipino": "tl",
    "finnish": "fi", "french": "fr", "frisian": "fy", "galician": "gl",
    "georgian": "ka", "german": "de", "greek": "el", "gujarati": "gu",
    "haitian creole": "ht", "hausa": "ha", "hawaiian": "haw", "hebrew": "he",
    "hindi": "hi", "hmong": "hmn", "hungarian": "hu", "icelandic": "is",
    "igbo": "ig", "indonesian": "id", "irish": "ga", "italian": "it",
    "japanese": "ja", "javanese": "jw", "kannada": "kn", "kazakh": "kk",
    "khmer": "km", "korean": "ko", "kurdish": "ku", "kyrgyz": "ky",
    "lao": "lo", "latin": "la", "latvian": "lv", "lithuanian": "lt",
    "luxembourgish": "lb", "macedonian": "mk", "malagasy": "mg", "malay": "ms",
    "malayalam": "ml", "maltese": "mt", "maori": "mi", "marathi": "mr",
    "mongolian": "mn", "myanmar": "my", "nepali": "ne", "norwegian": "no",
    "nyanja": "ny", "odia": "or", "pashto": "ps", "persian": "fa",
    "polish": "pl", "portuguese": "pt", "punjabi": "pa", "romanian": "ro",
    "russian": "ru", "samoan": "sm", "scots gaelic": "gd", "serbian": "sr",
    "sesotho": "st", "shona": "sn", "sindhi": "sd", "sinhala": "si",
    "slovak": "sk", "slovenian": "sl", "somali": "so", "spanish": "es",
    "sundanese": "su", "swahili": "sw", "swedish": "sv", "tajik": "tg",
    "tamil": "ta", "telugu": "te", "thai": "th", "turkish": "tr",
    "ukrainian": "uk", "urdu": "ur", "uzbek": "uz", "vietnamese": "vi",
    "welsh": "cy", "xhosa": "xh", "yiddish": "yi", "yoruba": "yo",
    "zulu": "zu"
}

@translate_bp.route('/api/translate/<int:id>', methods=['POST'])
@login_required
def translate_transcript(id):
    transcript = Transcript.query.get(id)
    if not transcript or transcript.user_id != current_user.id:
        return jsonify({'error': 'Transcript not found'}), 404

    requested_lang = request.json.get("language", "french").strip().lower()
    target_lang = LANGUAGE_MAP.get(requested_lang, requested_lang)

    # Limit to 1000 chars to avoid MyMemory failure
    text = transcript.text.strip()[:1000]
    if not text:
        return jsonify({'error': 'Transcript is empty or too short to translate.'}), 400

    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"en|{target_lang}",
            "key": MYMEMORY_API_KEY
        }

        res = requests.get(url, params=params)
        data = res.json()
        print("🔍 MyMemory response:", data)

        translated = data.get("responseData", {}).get("translatedText")
        if translated:
            return jsonify({
                "translated_text": translated,
                "language": target_lang
            })
        else:
            return jsonify({'error': 'Translation failed. MyMemory returned no result.'}), 500

    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500
