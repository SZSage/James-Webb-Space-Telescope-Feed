import React from "react";
import './Button.css';
import { Link } from 'react-router-dom'
/*
Button.js is the javascript file that is tasked with creating the BVbutton component that is used throughout the NebulaNet Webpage.
It was created as a component to allow easy integration into any subpage that needs some sort of button component.
It calls its corresponding css file for style reference and utilizes the react library
*/
const STYLES = ['btn--primary', 'btn--outline'];
const SIZES = ['btn--medium', 'btn--large'];


export const Button = ({children, type, onClick, buttonStyle, buttonSize
}) => {
    const checkButtonStyle = STYLES.includes(buttonStyle) ? buttonStyle : STYLES[0];

    const checkButtonSize = SIZES.includes(buttonSize) ? buttonSize : SIZES[0];

    return (
        <Link to='/about' className='btn-mobile'>
            <button
                className={`btn ${ checkButtonStyle } ${ checkButtonSize }`}
                onClick={onClick}
                type={type}
                >
                    {children}
            </button>

        </Link>
    )
}
