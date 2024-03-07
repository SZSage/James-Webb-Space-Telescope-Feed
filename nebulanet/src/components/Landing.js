import React from "react";
import { Button } from "./Button";
import './Landing.css';
import Carousel from "./Carousel.jsx";
import slides from "./pics.json";
import App from "./test.jsx";
/**
 Landing.js is a react component that is called by thge Home.js file within Pages that displays the carousel component and the associated information regarding the photo that
 is being viewed. It called both the Carousel copmponent and the Button component and renders each where needed. It also displays information detailing why out Fetch-process module
 chose infared as the .fit-to-.jpg file conversion
 */

function Landing() {
    return (
        <>
        <div className="landing-container">
            <video src="night-sky.mp4" autoPlay loop muted />
            <div className="contents">
                <h1>JWST Feed</h1>
                <p className="text">Check out the daily photo taken by the James Webb Space Telescope</p>
                <div className="landing-btn">
                    <Button className="land-btn" buttonStyle='btn--outline' buttonSize='btn--largel'>
                        Daily Photo
                    </Button>
               </div>
            </div>
        </div>
        </>
    )
}

export default Landing
