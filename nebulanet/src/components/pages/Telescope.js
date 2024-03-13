import React from "react";
import Footer from "../Footer.js";
import '../../App.js';
import RenderView from "../renderView.jsx";
import '../Model.css'
/*
Telescope is an intereseting subpage within NebulaNet as it allows the user to interact with a 3D model of the James Webb Telescope
and really get a solid visualization of what this inovative piece of technology looks like. This Telescope component calls the RenderView.js component
from the component directory and places it within the Telescope page along with the Footer component which exists on every page within NebulaNet.
*/
function Telescope () {
    return (
        <>
        <RenderView/>
        </>
  )
}
export default Telescope;
