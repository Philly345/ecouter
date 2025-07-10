import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './WelcomePage.css';

function WelcomePage() {
  const [name, setName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://localhost:5000/api/profile', { credentials: 'include' })
      .then((res) => res.json())
      .then((data) => {
        setName(data.name || 'there');
      })
      .catch(() => {
        setName('there');
      });
  }, []);

  const handleStart = () => {
    navigate('/dashboard');
  };

  return (
    <div className="welcome-container">
      <div className="welcome-box">
        <h1>Welcome, {name} 👋</h1>
        <p className="subtitle">
          Thanks for signing up! You're all set to start transcribing your audio files with Écouter.
        </p>
        <button onClick={handleStart} className="start-button">
          Go to Dashboard
        </button>
      </div>
    </div>
  );
}

export default WelcomePage;
