import React from 'react';
import '../styles/NavBar.css'

function Navbar() {
  return (
    <header>
      <nav>
        <ul>
          <li>
          <a href="/" style={{ display: 'flex', alignItems: 'center' }}>
            {/* <img src="logoinv.png" alt="Logo" /> */}
            <h1>Harmonized Landsat and Sentinel-2</h1>
          </a>
          </li>
        </ul>
      </nav>
    </header>

  );
}

export default Navbar;
