import React from "react";
import Landing from '../Landing.js';
import Footer from '../Footer.js';
import '../../App.js';
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
            <Footer />
        </>
    )
}
export default Home
