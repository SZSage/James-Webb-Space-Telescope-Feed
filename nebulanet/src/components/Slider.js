import React, { useState } from "react";
import SliderContent from "./SliderContent";
import Arrows from "./Arrows";
import Dots from "./Dots";
import "./slider.css"

/*
Slider.js is component that is called by Carousel.jsx and provides the logic for the carouselto know what photo
is currently being displayed and also provides funcionality to the arrows that are displayed for the user to be able to control which
photo they would like to view. the default photo that is shown upon loading Home.js is the most recent picture that the James
Webb Telescope has taken.
*/
const len = carousel.length - 1;


function Slider(props) {
    const [activeIndex, setActiveIndex] = useState(0);
    const [carousel, setcarousel] = useState([])
    return (
        <div className="slider-container">
            <SliderContent activeIndex={activeIndex} imageSlider={carousel}/>
            <Arrows
            prevSlide={() =>
                setActiveIndex(activeIndex < 1 ? len : activeIndex -1)
            }
            nextSlide={() =>
                setActiveIndex(activeIndex === len ? 0 : activeIndex +1)
            }
            />
            <Dots
                activeIndex={activeIndex}
                carousel={carousel}
                onclick={activeIndex => setActiveIndex(activeIndex)}/>
        </div>
    )
}
export default Slider
