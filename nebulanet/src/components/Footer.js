import React from 'react'
import './Footer.css'
import { Link } from 'react-router-dom';

/*
Footer.js is a component that is utilized by every subpage within NebulaNet as it contains the information regarding the site and its
creation. It helps with creating a offical look to the site and gives each page a visual end object so the user can be sure that
they have reached the end of the webpage and have viewed all of its content
 */
function Footer() {
  return (
    <>
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
                    <div className="box">
                        <img src="atom-8px.png" alt="atom" />
                    </div>
                </Link>
          </div>
          <small class='website-rights'>NebulaNet © 2024</small>
    </div>
    </>
  )
}

export default Footer
