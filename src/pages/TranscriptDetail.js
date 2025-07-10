import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const TranscriptDetail = () => {
  const { id } = useParams();
  const [transcript, setTranscript] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`http://localhost:5000/api/transcripts/${id}`, {
      credentials: 'include',
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          setError(data.error);
        } else {
          setTranscript(data);
        }
      })
      .catch(err => {
        console.error("Error fetching transcript:", err);
        setError("Failed to load transcript.");
      });
  }, [id]);

  if (error) {
    return <div className="p-8 text-red-500">Error: {error}</div>;
  }

  if (!transcript) {
    return <div className="p-8 text-white">Loading transcript...</div>;
  }

  return (
    <div style={{ padding: '30px', backgroundColor: '#121212', minHeight: '100vh', color: 'white' }}>
      <div style={{
        backgroundColor: '#1e1e1e',
        borderRadius: '8px',
        padding: '20px',
        maxWidth: '900px',
        margin: '0 auto',
        boxShadow: '0 0 8px rgba(0,0,0,0.3)'
      }}>
        <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '10px' }}>
          {transcript.filename}
        </h2>
        <p><strong>Status:</strong> {transcript.status}</p>
        <p><strong>Created:</strong> {new Date(transcript.created_at).toLocaleString()}</p>
        <hr style={{ borderTop: '1px solid #555', margin: '20px 0' }} />

        <div style={{
          whiteSpace: 'pre-wrap',
          fontSize: '16px',
          lineHeight: '1.6',
          color: '#ddd',
          backgroundColor: '#1b1b1b',
          padding: '15px',
          borderRadius: '6px'
        }}>
          {transcript.text}
        </div>
      </div>
    </div>
  );
};

export default TranscriptDetail;
