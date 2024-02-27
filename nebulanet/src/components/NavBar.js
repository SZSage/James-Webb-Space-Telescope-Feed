import React, {useState} from "react";
import { Link } from 'react-router-dom';
import './NavBar.css';


function NavBar() {
    const [click, setClick] = useState(false);
    const[button, setButton] = useState(true)

    const handleClick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false)


    const showButton = () => {
        if(window.innerWidth <= 960) {
            setButton(false);
        } else {
            setButton(true)
        }
    };
    window.addEventListener('resize', showButton)
  return (
    <>
        <nav className="Navbar">
            <div className="Navbar-container">
                <Link to='/' className="navbar-logo" onClick={closeMobileMenu}>
                    NebulaNet
                    <div className="box">
                        <img src="atom-8px.png" alt="atom" />
                    </div>
                </Link>
                <div className="menu-icon" onClick={handleClick}>
                    <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
                </div>
                <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                    <li className="nav-item">
                        <Link to='/' className="nav-links" onClick={closeMobileMenu}>
                            Home
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link to='/' className="nav-links" onClick={closeMobileMenu}>
                           Calendar
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link to='/' className="nav-links" onClick={closeMobileMenu}>
                           Sources
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link to='/about' className="nav-links" onClick={closeMobileMenu}>
                          About
                        </Link>
                    </li>
                </ul>
            </div>
        </nav>
    </>
  );
}

export default NavBar
