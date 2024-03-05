import React from 'react';
import './SourcesJS.css';
import RenderView from "./renderView.jsx";

/*
Sources.js is a component that will be called by Sources.js within the pages directory and will display all sources we used to opbtain the data that is beiing displayed all over the website
as well as information regarding the AWS support that we have created to allow us to host NebulaNet 24/7 and accessible to anyone
*/
function SourcesJS () {
  return (
    <div className="sourcesJS-container">
      <video className="video2" src="vid2background.mp4" autoPlay loop muted />
      <div className="overlay2"></div>
        <div className="contents2">
          <h1>Sources</h1>
      </div>
      <div className='subcontents'>
          <p className="bio">
            This is the sources page that will talk about all the technology and significance of the
            James Webb Space Telescope
          </p>
     </div>

    </div>
  )
}

export default SourcesJS
