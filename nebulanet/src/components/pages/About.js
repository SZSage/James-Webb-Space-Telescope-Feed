import React from "react";
import Footer from "../Footer.js";
import AboutDes from "../AboutDes.js";
import '../../App.js';
/*
About.js is the main component for the About page and calls the AboutDes and Footer component to create the entire About
landing page. This approach helps the component structure of react websites and allows for easy and effiecient creationg of different
pages with exisiting components that can be modified or called as is into said page. About.js is called by App.js in order to display the
About page using the react-router-dom library.
*/
function About () {
    return (
        <>
            <AboutDes />
            <Footer />

        </>
    )
}

export default About
