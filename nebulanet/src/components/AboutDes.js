import React from "react";
import './AboutDes.css';



function AboutDes () {
    return (
        <div className="about-container">
            <video className="vid" id="video-background" src="sunset-sky.mp4"/>
            <div className="overlay"></div>
            <div className="description">
             <p className="para">This project envisions a website dedicated to provide the latest observations and discoveries captured
                by the James Webb Space Telescope (JWST), sourced directly from the Mikulski Archive for Space Telescopes
                (MAST) database. It aims to serve as an interactive and educational portal where users can explore high
                definition visuals of galaxies, stars, planets, and other celestial phenomena. Each image will be
                accompanied by detailed information, including the scientific insights it provides, the specific JWST
                instruments involved in its capture, and other technical data.

                This website is designed to be both educational and engaging, enabling users of all backgrounds to
                view and learn about these discoveries.
            </p>
            </div>
        </div>
    )
}

export default AboutDes
