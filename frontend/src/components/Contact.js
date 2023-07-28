import React from 'react';
import '../styles/Contact.css';

const ContactSection = () => {
  return (
    <section className="contact-section">
      <h2>Contact Information</h2>
      <div className="contact-info">
        <div className="contact-logo">
          <img src="logoinv.png" alt="Logo" />
        </div>
        <div className="contact-details">
          <p>
            <i className="fas fa-envelope"></i>{' '}
            <strong>Email:</strong> <a href="mailto:hls-impact@uah.edu">hls-impact@uah.edu</a>
          </p>
          <p>
            <i className="fas fa-map-marker-alt"></i>{' '}
            320 Sparkman Drive NW Huntsville, AL 35805
          </p>
          <p>
            <i className="fas fa-phone"></i>
            256-961-70000
          </p>
        </div>
      </div>

    </section>
  );
};

export default ContactSection;
