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
      <div className="subcontents">
          <h1>Sources</h1>
      <hr classname="solid"/>
      </div>
      <div className="description">
        <h3>Main Resources for accessing JWST data and instrument data</h3>
        <a className="links" href="https://jwst-docs.stsci.edu/">https://jwst-docs.stsci.edu/</a>
        <h3>MAST queries using Astroquery Docs</h3>
        <a className="links" href="https://astroquery.readthedocs.io/en/latest/mast/mast.html">https://astroquery.readthedocs.io/en/latest/mast/mast.html</a>
        <h3>Interacting with MAST API</h3>
        <a className="links" href="https://outerspace.stsci.edu/display/MASTDOCS/Using+MAST+APIs#UsingMASTAPIs-AstroquerySearchandRetrieval">https://outerspace.stsci.edu/display/MASTDOCS/Using+MAST+APIs#UsingMASTAPIs-AstroquerySearchandRetrieval</a>
        <h3>FIT files and metadata extraction/handeling</h3>
        <a className="links" href="https://mast.stsci.edu/api/v0/_jwst_inst_keywd.html">https://mast.stsci.edu/api/v0/_jwst_inst_keywd.html</a>
        <a className="links" href="https://mast.stsci.edu/api/v0/_c_a_o_mfields.html">https://mast.stsci.edu/api/v0/_c_a_o_mfields.html</a>
        <a className="links" href="https://docs.astropy.org/en/stable/io/fits/index.html">https://docs.astropy.org/en/stable/io/fits/index.html</a>
        <h3>Streaming FITS data onto memory</h3>
        <a className="links" href="https://docs.python.org/3/library/io.html">https://docs.python.org/3/library/io.html</a>
        <h3>Scaling FITS data</h3>
        <a className="links" href="https://astromsshin.github.io/science/code/Python_fits_image/index.html">https://astromsshin.github.io/science/code/Python_fits_image/index.html</a>
      </div>

    </div>
  )
}

export default SourcesJS
