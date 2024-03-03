import React from 'react'
import './Footer.css'
import { Link } from 'react-router-dom';
function Footer() {
  return (
    <div className='footer-container'>
        <p>
            This website was created for CS 422 during Winter 2024 at the University of Oregon. </p>
        <p>Made by Simon Zhao, Jacob Burke, Daniel Willard, Isabella Cortez, and Freddy Lopez.
        </p>
        <div className='extra'>
            Clearly the sky isn't the limit
        </div>
        <div class='footer-logo'>
            <Link to='/' className="navbar-logo" >
                    NebulaNet
                    <div className="box">
                        <img src="atom-8px.png" alt="atom" />
                    </div>
                </Link>
          </div>
          <small class='website-rights'>NebulaNet © 2024</small>
    </div>
  )
}

export default Footer
