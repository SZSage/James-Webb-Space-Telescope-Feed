import React, { useState } from "react";
import SliderContent from "./SliderContent";
import Arrows from "./Arrows";
import Dots from "./Dots";
import carousel from "./carousel";
import "./slider.css"

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
