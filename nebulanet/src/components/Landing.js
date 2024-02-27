import React from "react";
import { Link } from 'react-router-dom';
import { Button } from "./Button";
import './Landing.css';



function Landing() {
    return (
        <div className="landing-container">
            <video src="night-sky.mp4" autoPlay loop muted />
            <div className="contents">
                <h1>JWST Feed</h1>
                <p className="text">Check out the daily photo taken by the James Webb Telescope</p>
                <div className="landing-btn">
                    <Button className="land-btn" buttonStyle='btn--outline' buttonSize='btn--largel'>
                        Daily Photo
                    </Button>
               </div>
            </div   >
        </div>
    )
}

export default Landing
