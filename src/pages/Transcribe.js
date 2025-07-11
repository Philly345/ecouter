import React, { useState, useRef, useEffect } from 'react';
import './Transcribe.css';

function Transcribe() {
  const [file, setFile] = useState(null);
  const [verbatim, setVerbatim] = useState(false);
  const [diarization, setDiarization] = useState(false);
  const [language, setLanguage] = useState('en');
  const [tags, setTags] = useState('');
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState('');

  const [transcript, setTranscript] = useState(localStorage.getItem('transcript') || '');
  const [audioUrl, setAudioUrl] = useState(localStorage.getItem('audioUrl') || '');
  const [wordList, setWordList] = useState(JSON.parse(localStorage.getItem('wordList')) || []);
  const [loading, setLoading] = useState(false);
  const [activeWordIndex, setActiveWordIndex] = useState(null);
  const [processingTranscriptId, setProcessingTranscriptId] = useState(localStorage.getItem('processingId'));

  const audioRef = useRef(null);

  const languageOptions = [
    { code: 'en', name: 'English' },
    { code: 'fr', name: 'French' },
    { code: 'es', name: 'Spanish' },
    { code: 'sw', name: 'Swahili' },
    { code: 'de', name: 'German' },
    { code: 'ar', name: 'Arabic' },
    { code: 'hi', name: 'Hindi' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ru', name: 'Russian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'it', name: 'Italian' },
    { code: 'ko', name: 'Korean' },
    { code: 'ja', name: 'Japanese' },
    { code: 'tr', name: 'Turkish' },
    { code: 'nl', name: 'Dutch' },
    { code: 'pl', name: 'Polish' },
    { code: 'uk', name: 'Ukrainian' },
    { code: 'el', name: 'Greek' },
    { code: 'he', name: 'Hebrew' },
    { code: 'bn', name: 'Bengali' },
    { code: 'ta', name: 'Tamil' },
    { code: 'ur', name: 'Urdu' },
    { code: 'zu', name: 'Zulu' },
    { code: 'am', name: 'Amharic' },
    { code: 'yo', name: 'Yoruba' }
  ];

  useEffect(() => {
    fetch('http://localhost:5000/api/projects', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setProjects(data))
      .catch(err => console.error("Failed to load projects:", err));
  }, []);

  const pollTranscriptStatus = async (id) => {
    try {
      const res = await fetch(`http://localhost:5000/api/transcripts/${id}`, {
        credentials: 'include',
      });
      const data = await res.json();

      if (data.status === 'complete') {
        setTranscript(data.text);
        const fullAudioUrl = `http://localhost:5000${data.audio_url}`;
        setAudioUrl(fullAudioUrl);

        const allWords = [];
        data.word_timings?.forEach(segment => {
          if (segment.words) {
            segment.words.forEach(word => allWords.push(word));
          }
        });
        setWordList(allWords);

        localStorage.setItem('transcript', data.text);
        localStorage.setItem('audioUrl', fullAudioUrl);
        localStorage.setItem('wordList', JSON.stringify(allWords));
        localStorage.removeItem('processingId');
        setProcessingTranscriptId(null);
      } else {
        setTimeout(() => pollTranscriptStatus(id), 5000);
      }
    } catch (error) {
      console.error('Polling error:', error);
    }
  };

  const handleSubmit = async () => {
    if (!file) return alert("Please choose a file.");

    setLoading(true);
    setTranscript('');
    setAudioUrl('');
    setWordList([]);
    localStorage.clear();

    const formData = new FormData();
    formData.append('file', file);
    formData.append('verbatim', verbatim);
    formData.append('diarization', diarization);
    formData.append('language', language);

    if (selectedProjectId) {
      formData.append('project_id', selectedProjectId);
    }

    tags.split(',').map(tag => tag.trim()).filter(tag => tag).forEach(tag => {
      formData.append('tags', tag);
    });

    try {
      const response = await fetch('http://localhost:5000/api/transcribe', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      const data = await response.json();

      if (response.ok) {
        if (data.status === 'processing') {
          setProcessingTranscriptId(data.id);
          localStorage.setItem('processingId', data.id);
          pollTranscriptStatus(data.id);
        } else {
          setTranscript(data.transcript);
          setAudioUrl(data.audio_url);

          const allWords = [];
          data.word_timings?.forEach(segment => {
            if (segment.words) {
              segment.words.forEach(word => allWords.push(word));
            }
          });
          setWordList(allWords);

          localStorage.setItem('transcript', data.transcript);
          localStorage.setItem('audioUrl', data.audio_url);
          localStorage.setItem('wordList', JSON.stringify(allWords));
        }
      } else {
        alert(data.error || 'Transcription failed.');
      }
    } catch (err) {
      console.error('Transcription error:', err);
      alert('An error occurred while transcribing the file.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !wordList.length) return;

    const onTimeUpdate = () => {
      const currentTime = audio.currentTime;
      const index = wordList.findIndex(word =>
        currentTime >= word.start && currentTime <= word.end
      );
      setActiveWordIndex(index);
    };

    audio.addEventListener('timeupdate', onTimeUpdate);
    audio.addEventListener('ended', () => setActiveWordIndex(null));
    return () => {
      audio.removeEventListener('timeupdate', onTimeUpdate);
      audio.removeEventListener('ended', () => setActiveWordIndex(null));
    };
  }, [wordList]);

  useEffect(() => {
    if (processingTranscriptId) {
      pollTranscriptStatus(processingTranscriptId);
    }
  }, []);

  const isWordLevel = wordList.length > 0 && wordList.every(w => w.word || w.text);

  return (
    <div className="transcribe-container">
      <h2>Transcribe Audio File</h2>

      <div className="transcribe-box">
        <div className="transcribe-field">
          <label>Upload Audio/Video:</label>
          <input type="file" accept="audio/*,video/*" onChange={(e) => setFile(e.target.files[0])} />
        </div>

        <div className="transcribe-checkboxes">
          <label>
            <input type="checkbox" checked={verbatim} onChange={() => setVerbatim(!verbatim)} />
            Verbatim transcription
          </label>

          <label>
            <input type="checkbox" checked={diarization} onChange={() => setDiarization(!diarization)} />
            Identify speakers
          </label>

          <label>
            Language:
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
              {languageOptions.map(lang => (
                <option key={lang.code} value={lang.code}>{lang.name}</option>
              ))}
            </select>
          </label>
        </div>

        <div className="transcribe-field">
          <label>Assign to Project:</label>
          <select value={selectedProjectId} onChange={(e) => setSelectedProjectId(e.target.value)}>
            <option value="">None</option>
            {projects.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>

        <div className="transcribe-field">
          <label>Tags (comma separated):</label>
          <input type="text" value={tags} onChange={(e) => setTags(e.target.value)} placeholder="e.g. meeting, client, sales" />
        </div>

        <button onClick={handleSubmit} disabled={loading}>
          {loading ? 'Transcribing...' : 'Transcribe'}
        </button>
      </div>

      {audioUrl && (
        <div className="audio-preview">
          <h3>Play Audio:</h3>
          <audio ref={audioRef} controls src={audioUrl}></audio>
        </div>
      )}

      {transcript && (
        <div className="transcript-output">
          <h3>Transcript:</h3>
          {isWordLevel ? (
            <div className="word-highlighting">
              {wordList.map((word, index) => (
                <span key={index} className={index === activeWordIndex ? 'highlight' : ''}>
                  {(word.word || word.text || '[?]') + ' '}
                </span>
              ))}
            </div>
          ) : (
            <div className="paragraph-format">
              {transcript.split('\n\n').map((para, i) => (
                <p key={i}>{para}</p>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Transcribe;
