import React from "react";
import Landing from '../Landing.js';
import Footer from '../Footer.js';
import '../../App.js';
import App from "../test.jsx"
import "./Home.css";
import Welcome from "../Wecome.js";
/*
Home.js is the main component for the About page and calls the Landing and Footer component to create the entire Home
landing page. This approach helps the component structure of react websites and allows for easy and effiecient creationg of different
pages with exisiting components that can be modified or called as is into said page. Home.js is called by App.js in order to display the
homepage using the react-router-dom library.
*/

function Home () {
    return (
        <>
            <Landing/>
            <Welcome/>
            <App/>
        <div className="explain">
            <h3>WHY IS WEBB AN INFRARED TELESCOPE?</h3>
            <p className="explain-desc">
                By viewing the universe at infrared wavelengths Webb is now showing us things never before
                seen by any other telescope. It is only at infrared wavelengths that we can see the first stars
                and galaxies forming after the Big Bang. And it is with infrared light that we can see stars and
                planetary systems forming inside clouds of dust that are opaque to visible light.

                The primary goals of Webb are to study galaxy, star and planet formation in the universe. To see
                the very first stars and galaxies that formed in the early universe, we have to look deep into space
                to look back in time (because it takes light time to travel from there to here, the farther out we look,
                the further we look back in time).

                The universe is expanding, and therefore the farther we look, the faster objects are moving away from us,
                redshifting the light. Redshift means that light that is emitted as ultraviolet or visible light is shifted
                more and more to redder wavelengths, into the near- and mid-infrared part of the electromagnetic spectrum
                for very high redshifts. Therefore, to study the earliest star and galaxy formation in the universe, we
                have to observe infrared light and use a telescope and instruments optimized for this light.

                Star and planet formation in the local universe takes place in the centers of dense, dusty clouds,
                obscured from our eyes at normal visible wavelengths. Near-infrared light, with its longer wavelength,
                is less hindered by the small dust particles, allowing near-infrared light to escape from the dust clouds.
                By observing the emitted near-infrared light we can penetrate the dust and see the processes leading to
                star and planet formation.

                Objects of about Earth's temperature emit most of their radiation at mid-infrared wavelengths. These
                temperatures are also found in dusty regions forming stars and planets, so with mid-infrared radiation
                we can see the glow of the star and planet formation taking place. An infrared-optimized telescope allows
                us to penetrate dust clouds to see the birthplaces of stars and planets.
            </p>
        </div>
            <Footer />
        </>
    )
}
export default Home
