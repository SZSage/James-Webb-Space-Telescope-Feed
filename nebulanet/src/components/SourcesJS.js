import React from "react";
import "./SourcesJS.css"

function SourcesJS () {
    return (
        <>
            <video src="night-sky.mp4" autoPlay loop muted />
            <div className="wrapperSource">
                <h1>Sources</h1>
                <div className="link-cont">
                  <h3>Photo and Metadata Coalescence Module</h3>
                  <h2>Accessing JWST data</h2>
                  <a className="links" href="https://jwst-docs.stsci.edu/">jwst-docs/</a>
                  <h2>MAST queries using Astroquery Docs</h2>
                  <a className="links" href="https://astroquery.readthedocs.io/en/latest/mast/mast.html">astroquery docs</a>
                  <h2>Interacting with MAST API</h2>
                  <a className="links" href="https://outerspace.stsci.edu/display/MASTDOCS/Using+MAST+APIs#UsingMASTAPIs-AstroquerySearchandRetrieval">Astroquery Search and Retrieval</a>
                  <h2>FIT files and metadata extraction/handeling</h2>
                  <a className="links" href="https://mast.stsci.edu/api/v0/_c_a_o_mfields.html">https://mast.stsci.edu/api/v0/_c_a_o_mfields.html</a>
                  <a className="links" href="https://docs.astropy.org/en/stable/io/fits/index.html">https://docs.astropy.org/en/stable/io/fits/index.html</a>
                  <h2>Streaming FITS data onto memory</h2>
                  <a className="links" href="https://docs.python.org/3/library/io.html">https://docs.python.org/3/library/io.html</a>
                  <h2>Scaling FITS data</h2>
                  <a className="links" href="https://astromsshin.github.io/science/code/Python_fits_image/index.html">Python fits image</a>


                  <h3>Web Hosting Module</h3>
                  <h2>AWS SDK Python library</h2>
                  <a className="links" href="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html">Amazon AWS Documentation</a>
                  <h2>Amazon Web Services</h2>
                  <a className="links" href="https://github.com/open-guides/og-aws">Open Guides GitHub</a>
                  <h2>Static Hosting via AWS</h2>
                  <a className="links" href="https://victoria.dev/blog/hosting-your-static-site-with-aws-s3-route-53-and-cloudfront/">AWS S3, route 53, and Cloudfront</a>
                  <a className="links" href="https://www.freecodecamp.org/news/a-beginners-guide-on-how-to-host-a-static-site-with-aws/">FreeCodeCamp - Static AWS Hosting</a>


                  <h3>Mission information Gatherer Module</h3>
                  <h2>Observation Schedules</h2>
                  <a className="links" href="https://www.stsci.edu/jwst/science-execution/observing-schedules">James Webb Obesrvation Schedules</a>
                  <h2>Amazon Web Services</h2>
                  <a className="links" href="https://github.com/open-guides/og-aws">Open Guides GitHub</a>
                  <h2>Static Hosting via AWS</h2>
                  <a className="links" href="https://victoria.dev/blog/hosting-your-static-site-with-aws-s3-route-53-and-cloudfront/">AWS S3, route 53, and Cloudfront</a>
                  <a className="links" href="https://www.freecodecamp.org/news/a-beginners-guide-on-how-to-host-a-static-site-with-aws/">FreeCodeCamp - Static AWS Hosting</a>




                </div>

            </div>
        </>
    )
}
export default SourcesJS
