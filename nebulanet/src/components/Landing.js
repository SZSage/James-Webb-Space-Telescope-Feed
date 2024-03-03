import React from "react";
import { Button } from "./Button";
import './Landing.css';
import Carousel from "./Carousel.jsx";
import slides from "./pics.json";


function Landing() {
    return (
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
            <div className="picCar">
                <Carousel data={slides}/>
            </div>
        </div>
    )
}

export default Landing
