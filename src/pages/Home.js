import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Logo from '../Assets/Logo.svg';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();
  const [theme, setTheme] = useState('dark');

  const subtitle = 'Transcribe audio like never before.';

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
    document.body.classList.toggle('light-theme');
  };

  const roles = [
    {
      label: 'Doctors',
      description: 'Medical notes, patient interviews',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round">
          <path d="M12 2v20M2 12h20" />
        </svg>
      )
    },
    {
      label: 'Nurses',
      description: 'Clinical observations',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round">
          <path d="M12 2v4M9 6h6M4 10h16v10H4z" />
        </svg>
      )
    },
    {
      label: 'Lawyers',
      description: 'Depositions, interviews',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
          <path d="M12 2l4 8H8l4-8zM6 12h12v10H6z" />
        </svg>
      )
    },
    {
      label: 'Students',
      description: 'Lectures & study sessions',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
          <path d="M2 6l10-4 10 4-10 4L2 6z" />
          <path d="M12 10v10" />
          <path d="M4 14s4 2 8 2 8-2 8-2" />
        </svg>
      )
    },
    {
      label: 'Podcasters',
      description: 'Episodes & interviews',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
          <circle cx="12" cy="12" r="3" />
          <path d="M19.5 12a7.5 7.5 0 0 0-15 0" />
          <path d="M16.5 12a4.5 4.5 0 0 0-9 0" />
        </svg>
      )
    },
    {
      label: 'Journalists',
      description: 'Interviews & field notes',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
          <rect x="3" y="4" width="18" height="16" rx="2" />
          <line x1="7" y1="8" x2="17" y2="8" />
          <line x1="7" y1="12" x2="17" y2="12" />
          <line x1="7" y1="16" x2="12" y2="16" />
        </svg>
      )
    }
  ];

  return (
    <main className={`home-container ${theme === 'light' ? 'light-theme' : ''}`}>
      {/* HERO SECTION */}
      <section className="hero-section bubble-bg fade-in">
        <img
          src={Logo}
          alt="Écouter.ai Logo"
          className="hero-logo live-logo-button bounce"
          onClick={() => navigate('/')}
        />
        <h1 className="welcome-title">
          Welcome to <span className="gradient-text">Écouter.ai</span>
        </h1>
        <p className="subtitle">{subtitle}</p>
        <p className="pitch-text">
          Built for <strong>doctors</strong>, <strong>nurses</strong>, <strong>lawyers</strong>,{' '}
          <strong>students</strong>, <strong>podcasters</strong>, and <strong>journalists</strong>. Start transcribing instantly — <strong>no payment</strong>, <strong>no credit card</strong> required.
        </p>
        <button className="get-started-bubble shiny-button" onClick={() => navigate('/signup')}>
          Get Started
        </button>
        <div className="scroll-indicator animate-bounce">▼</div>
      </section>

      {/* WHO IS IT FOR */}
      <section className="roles-section fade-in">
        <h2 className="features-title">Who Is It For?</h2>
        <div className="roles-grid">
          {roles.map((role, index) => (
            <div className="role-card" key={index}>
              <div className="feature-icon">{role.icon}</div>
              <span>{role.label}</span>
              <p className="role-description">{role.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* FEATURES */}
      <section className="features-section fade-in">
        <h2 className="features-title">Why Choose Écouter.ai?</h2>
        <div className="features-grid">
          <div className="feature-item">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2a5 5 0 0 0-5 5v1H6a2 2 0 0 0 0 4h1v2H6a2 2 0 0 0 0 4h1v1a5 5 0 0 0 5 5" />
              <path d="M12 2a5 5 0 0 1 5 5v1h1a2 2 0 0 1 0 4h-1v2h1a2 2 0 0 1 0 4h-1v1a5 5 0 0 1-5 5" />
            </svg>
            <h3>AI-Powered Transcription</h3>
            <p>Harness cutting-edge artificial intelligence to transcribe speech with unmatched accuracy.</p>
          </div>

          <div className="feature-item">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round">
              <line x1="4" y1="12" x2="4" y2="12" />
              <line x1="8" y1="8" x2="8" y2="16" />
              <line x1="12" y1="4" x2="12" y2="20" />
              <line x1="16" y1="8" x2="16" y2="16" />
              <line x1="20" y1="12" x2="20" y2="12" />
            </svg>
            <h3>Crystal-Clear Transcriptions</h3>
            <p>AI-powered accuracy that captures every word—every time.</p>
          </div>

          <div className="feature-item">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <line x1="2" y1="12" x2="22" y2="12" />
              <path d="M12 2a15.3 15.3 0 0 1 0 20" />
              <path d="M12 2a15.3 15.3 0 0 0 0 20" />
            </svg>
            <h3>Multilingual Support</h3>
            <p>Transcribe in over 40 languages with fluent-level precision.</p>
          </div>

          <div className="feature-item">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            <h3>GPT Smart Summaries</h3>
            <p>Instantly turn transcripts into clean, digestible summaries.</p>
          </div>

          <div className="feature-item">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 6h5l2 3h11v11H3z" />
            </svg>
            <h3>Project Organization</h3>
            <p>Stay on top of your files with tagging and folder-based organization.</p>
          </div>
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className="testimonials-section fade-in">
        <h2 className="features-title">What Our Users Say</h2>
        <div className="testimonial-list floating">
          <article className="testimonial" style={{ animationDelay: '0.2s' }}>
            <p>“Écouter.ai is a game-changer for my podcast episodes. So easy and fast!”</p>
            <cite>- Alex R., Podcaster</cite>
          </article>
          <article className="testimonial" style={{ animationDelay: '0.6s' }}>
            <p>“Finally, a tool that actually works. No payments, just results.”</p>
            <cite>- Monica W., Journalist</cite>
          </article>
          <article className="testimonial" style={{ animationDelay: '1s' }}>
            <p>“As a student, I use it all the time for lectures. Love it!”</p>
            <cite>- Jordan K., Student</cite>
          </article>
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section fade-in">
        <h2 className="features-title">Ready to Get Started?</h2>
        <p>Join thousands who transcribe faster and smarter with Écouter.ai.</p>
        <button className="get-started-bubble shiny-button" onClick={() => navigate('/signup')}>
          Sign Up Free
        </button>
      </section>

      {/* CONTACT */}
      <section className="contact-section fade-in">
        <h2 className="features-title">Contact Us</h2>
        <p>Email: <a href="mailto:ecouter.transcribe@gmail.com">ecouter.transcribe@gmail.com</a></p>
        <p>Instagram: <a href="https://instagram.com/ecouter.ai" target="_blank" rel="noreferrer">@ecouter.ai</a></p>
      </section>

      {/* FOOTER */}
      <footer className="footer-section">
        <div className="footer-container">
          <p>&copy; {new Date().getFullYear()} Écouter.ai. All rights reserved.</p>
          <div className="footer-links">
            <a href="https://instagram.com/ecouter.ai" target="_blank" rel="noreferrer">Instagram</a>
            <a href="mailto:ecouter.transcribe@gmail.com">Email</a>
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
          </div>
        </div>
      </footer>
    </main>
  );
};

export default Home;
