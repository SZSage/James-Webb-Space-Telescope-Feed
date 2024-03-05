import React, { useState } from 'react'
import "./Carousel.css"
import {BsArrowLeftCircleFill, BsArrowRightCircleFill} from 'react-icons/bs'
/*
Carousel.js is a major react component that is the essesence of showing the daily photos taken by the James Webb Teslescope
and is displayed on the Home page of the website NebulaNet. The component is called by Home.js within the pages directory and
is displayed accordingly wihtin the syle specifications noted in Carousel.css:w
*/

function Carousel ({data}) {
    console.log(data)
    const [slide, setSlide] = useState(0);

    const nextSlide = () => {
        setSlide(slide === data.length - 1 ? 0 : slide +1);
    };

    const prevSlide = () => {
        setSlide(slide === 0 ? data.length - 1 : slide -1);
    };


    return (
    <div className="carousel-container">
        <BsArrowLeftCircleFill onClick={prevSlide} className='arrow arrow-left'/>
        {data.slides.map((item, index) => {
            return (<>
            <img
            src={item.src}
            alt={item.title}
            key={index}
            className={slide === index ? "slide" : "slide slide-hidden"}
            />
            <p className={slide === index ? "picture-description" : "picture-description pic-hidden"}/>
            </>
            );
        })}
        <BsArrowRightCircleFill className='arrow arrow-right' onClick={nextSlide}/>
        <span className='indicators'>
            {data.slides.map((_, index) => {
                return (
                <button
                key={index}
                className={slide === index ? "indicator" : "indicator-inactive"}
                onClick={() => setSlide(index)}/>
                );
            })}
        </span>
    </div>
  )
}

export default Carousel
