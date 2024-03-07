import React from "react";
import "./Welcome.css";

function Welcome () {
    return (
        <>
            <div className="wrapper">
                <h1> Wecome to NebulaNet!</h1>
                <hr classname="solid"/>
                <div className="welcome">
                    NebulaNet aims to be a resource displaying the daily observations
                    taken by the James Webb Telescope. Contrary to popular belief, the
                    photos that many of us have seen are composity images made up of hundreds
                    of different individual photos using a variety of different of instruments
                    and image settings. These are then converted into png photos using different
                    algorithms depending on the tyoe of subject the image was focusing on.
                </div>
            </div>
        </>
    )
}
export default Welcome
