import React from 'react';

const Privacy = () => (
  <div className="privacy-container" style={{ padding: '40px', color: '#fff' }}>
    <h1>Privacy Policy</h1>

    <p>At Écouter.ai, we respect your privacy and are committed to protecting the personal data you share with us. This Privacy Policy outlines how we collect, use, store, and protect your information when you use our platform.</p>

    <h2>1. Information We Collect</h2>
    <ul>
      <li><strong>Account Information:</strong> Name, email address, password (hashed), and optional profile details.</li>
      <li><strong>Audio/Video Files:</strong> Files uploaded for transcription and associated metadata.</li>
      <li><strong>Usage Data:</strong> Interactions with our platform, including access times, pages viewed, and device/browser type.</li>
      <li><strong>Cookies:</strong> We use cookies to enhance user experience and track session information.</li>
    </ul>

    <h2>2. How We Use Your Information</h2>
    <ul>
      <li>To provide and improve our transcription and summarization services.</li>
      <li>To communicate with you about your account or support requests.</li>
      <li>To send occasional updates, announcements, or feature rollouts (if opted-in).</li>
      <li>To monitor platform usage and prevent fraud or abuse.</li>
    </ul>

    <h2>3. Third-Party Services</h2>
    <p>We partner with trusted services such as:</p>
    <ul>
      <li><strong>AssemblyAI:</strong> For audio transcription.</li>
      <li><strong>OpenAI:</strong> For AI summaries and processing.</li>
      <li><strong>Google Translate / MyMemory:</strong> For translation features.</li>
    </ul>
    <p>These services have their own privacy policies. We ensure data sent to them is encrypted and anonymized where possible.</p>

    <h2>4. Data Storage & Security</h2>
    <ul>
      <li>All user data and uploaded files are stored securely using encrypted cloud storage.</li>
      <li>Access to files is restricted to the account that uploaded them.</li>
      <li>We regularly audit our systems to ensure data security and integrity.</li>
    </ul>

    <h2>5. GDPR Compliance</h2>
    <p>If you are located in the European Economic Area (EEA), you have the right to:</p>
    <ul>
      <li>Access, correct, or delete your personal data.</li>
      <li>Withdraw consent or object to processing.</li>
      <li>Request data portability.</li>
    </ul>
    <p>To exercise these rights, contact us at <a href="mailto:ecouter.transcribe@gmail.com">ecouter.transcribe@gmail.com</a>.</p>

    <h2>6. HIPAA Disclaimer</h2>
    <p>Écouter.ai is not a HIPAA-covered entity. If you are using our platform to transcribe medical data or Protected Health Information (PHI), it is your responsibility to ensure compliance with HIPAA or local healthcare privacy laws. We do not currently offer a Business Associate Agreement (BAA).</p>

    <h2>7. Children’s Privacy</h2>
    <p>Écouter.ai is not intended for use by individuals under the age of 13. We do not knowingly collect personal information from children without parental consent.</p>

    <h2>8. Data Retention</h2>
    <p>Uploaded files and transcripts are retained until the user deletes them. You may contact us to request full deletion of your account and associated data.</p>

    <h2>9. Changes to This Policy</h2>
    <p>We may update this Privacy Policy from time to time. If we make significant changes, we will notify you via email or prominent notice on the website.</p>

    <h2>10. Contact</h2>
    <p>If you have questions or requests related to this policy, contact us:</p>
    <ul>
      <li>Email: <a href="mailto:ecouter.transcribe@gmail.com">ecouter.transcribe@gmail.com</a></li>
      <li>Instagram: <a href="https://instagram.com/ecouter.ai" target="_blank" rel="noreferrer">@ecouter.ai</a></li>
    </ul>
  </div>
);

export default Privacy;
