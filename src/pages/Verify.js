import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import './Verify.css';

function Verify() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [message, setMessage] = useState('Verifying your email...');
  const [error, setError] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    if (!token) {
      setError('Verification token is missing.');
      return;
    }

    const verifyEmail = async () => {
      try {
        const response = await fetch('http://localhost:5000/verify-email', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token }),
        });

        const data = await response.json();
        if (response.ok) {
          setMessage('✅ Email verified! Redirecting to login...');
          setTimeout(() => navigate('/login'), 2000);
        } else {
          setError(data.error || 'Verification failed.');
        }
      } catch (err) {
        setError('Network error. Please try again later.');
      }
    };

    verifyEmail();
  }, [searchParams, navigate]);

  return (
    <div className="verify-container">
      <h2>Email Verification</h2>
      {error ? (
        <p className="error-text">{error}</p>
      ) : (
        <p className="success-text">{message}</p>
      )}
    </div>
  );
}

export default Verify;
