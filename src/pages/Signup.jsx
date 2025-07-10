import React from 'react';
import './Signup.css';
import googleLogo from '.../Assests/google-icon.svg'; // Confirm this path is correct

function Signup() {
  return (
    <div className="signup-container">
      <h2>Sign Up to Écouter.ai</h2>

      <form className="signup-form">
        <input type="text" placeholder="Full Name" required />
        <input type="email" placeholder="Email" required />
        <input type="password" placeholder="Password" required />
        <input type="password" placeholder="Confirm Password" required />
      </form>

      <div className="signup-buttons">
        <button className="email-button">Continue with Email</button>

        <button className="google-button shine-hover">
          <img src={googleLogo} alt="Google" className="google-logo" />
          Continue with Google
        </button>
      </div>

      <div className="terms">
        <input type="checkbox" id="terms" />
        <label htmlFor="terms">
          I accept the <a href="#">terms and conditions</a>
        </label>
      </div>

      <p className="login-link">
        Already have an account? <a href="/login">Log in</a>
      </p>
    </div>
  );
}

export default Signup;
