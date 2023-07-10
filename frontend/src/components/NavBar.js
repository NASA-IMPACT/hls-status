import React from 'react';
import '../styles/NavBar.css'
import {HLS_TITLE} from '../utilities/config';

function Navbar() {
  return (
    <header>
      <nav>
        <ul>
          <li>
          <a href="/" style={{ display: 'flex', alignItems: 'center' }}>
            <img src="logoinv.png" alt="Logo" />
            <h1>{HLS_TITLE}</h1>
          </a>
          </li>
        </ul>
      </nav>
    </header>

  );
}

export default Navbar;
