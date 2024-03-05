import React from "react";
import './AboutDes.css';

/*
AboutDes.js is the javascript page that is tasked with creating the "About" subpage that is on NebulaNet. It consists of information regarding
the James Webb Telescope such as its purpose and important facts that set it apart from other telescopes that NASA uses

AboutDes.js is not directly displayed on the webpage but instead called by About.js wihtin the pages directory as a component for the sake of
modularity and organization. This file utilizes react and also calls its corresponding css file for stylistic purposes
*/

function AboutDes () {
    return (
        <>
        <div className="about-container">
            <video className="vid" src="sunset-sky.mp4" autoPlay loop muted/>
            <div className="title">
                <h1>What is the James Webb Space Telescope?</h1>
            <hr classname="solid"/>
            </div>

            <div className="description">
                <p className="facts">The James Webb Space Telescope, also called Webb or JWST, is a large, space-based observatory, optimized
                    for infrared wavelengths, which complements and extends the discoveries of the Hubble Space Telescope.
                    Webb launched on December 25, 2021, and its first full-color images and data were released to the world on
                    July 12, 2022.It covers longer wavelengths of light than Hubble and has greatly improved sensitivity.
                    The longer wavelengths enable Webb to look further back in time to see the first galaxies that formed
                    in the early universe, and to peer inside dust clouds where stars and planetary systems are forming today.
                    </p>
                <img className="diagram" src="realJSWT.jpg" width={1000}  />
                <p className="subtitle">*James Webb telescope’s 18-segmented gold mirror is specially designed to capture infrared light
                    from the first galaxies that formed in the early universe.</p>
                <p className="facts">
                    Webb studies every phase in the history of our Universe, ranging from the first luminous glows after the
                    Big Bang, to the formation of solar systems capable of supporting life on planets like Earth, to the
                    evolution of our own Solar System. Webb launched on Dec. 25th 2021. It does not orbit around the Earth
                    like the Hubble Space Telescope, it orbits the Sun 1.5 million kilometers (1 million miles) away from
                    he Earth at what is called the second Lagrange point or L2.
                </p>
                <img className="diagram" src="teleinfo.jpg"/>
                <h4>How does it differ compared to the famours Hubble Space Telescope?</h4>
                <p className="facts">
                    Webb is designed to look deeper into space to see the earliest stars and galaxies that formed in the universe
                    and to look deep into nearby dust clouds to study the formation of stars and planets.

                    In order to do this, Webb has a much larger primary mirror than Hubble (2.5 times larger in diameter, or about
                    6 times larger in area), giving it more light-gathering power. It also has infrared instruments with longer
                    wavelength coverage and greatly improved sensitivity than Hubble. Finally, Webb is operating much farther from Earth,
                    maintaining its extremely cold operating temperature, stable pointing and higher observing efficiency than the Earth-orbiting Hubble.

                </p>

            </div>
        </div>
        <div className="creator">
        <hr classname="solid"/>

        <p className="para">This project envisions a website dedicated to provide the latest observations and discoveries captured
                    by the James Webb Space Telescope (JWST), sourced directly from the Mikulski Archive for Space Telescopes
                    (MAST) database. It aims to serve as an interactive and educational portal where users can explore high
                    definition visuals of galaxies, stars, planets, and other celestial phenomena. Each image will be
                    accompanied by detailed information, including the scientific insights it provides, the specific JWST
                    instruments involved in its capture, and other technical data. </p>

        </div>
        </>
    )
}

export default AboutDes
