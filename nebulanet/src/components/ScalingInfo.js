import React from "react";
import './ScalingInfo.css';
import './Landing.css';
function ScalingInfo () {
    return (
            <div className="info-wrapper">
                <h5>JWST Project FITS Processing</h5>
                <div className="scaling-desc">
                    <h5>Overview</h5>
                    <p className="explain-desc">Astronomical observations were taken from the Mikulski Archive for Space Telescopes (MAST) database,
                        specifically for the James Webb Space Telescope (JWST). These observations are in the form of Flexible
                        Image Transportation System (FITS) file format which is a commonly used digital file format in astronomy.
                        FITS files contain image data formatted as multi-dimensional arrays, in this case 2D and 3D.
                        However, the raw form of these images often masks the important details necessary for scientific analysis.
                        The files are converted into a more visually accessible format like PNG.
                        However, simply converting FITS files to PNG images can result in a loss of detail, making it challenging to
                        discern important features. To overcome this, we employ various scaling techniques on the FITS files before
                        conversion. These methods are designed to enhance the visibility of details that might not be apparent in the
                        raw data.
                    <img className="diagram" src="fitsDataEx.png" alt="Example of raw .fit data"/>
                    </p>
                    <h5>Scaling Methods</h5>
                    <p className="explain-desc">
                        <p className="subTitle">Square Root Scaling</p>
                        This method involves taking the square root of each pixel value in the image. By applying this, the
                        square root scaling effectively compresses the dynamic range of the higher intensity values while
                        expanding the range of lower intensity values. This results in an image where dim features become more
                        visible against the background, aiding in the identification of subtle celestial structures.
                        <p className="subTitle">Histogram Equalization Scaling</p>
                        The histogram equalization scaling operates by adjusting the intensity distribution of the image's pixels.
                        This method first calculates the histogram of the pixel intensity values in the FITS file. Then, it creates a
                        cumulative distribution function (CDF) from this histogram, which maps the original pixel values to new
                        values that spread out the most frequent intensity values.
                        <p className="subTitle"></p>
                        This method enhances the contrast of the image by redistributing the pixel intensity values more evenly
                        across the histogram. This makes features that were previously hard to distinguish due to close intensity
                        values become more defined, significantly improving the image's overall clarity and detail.
                        <p className="subTitle">Application in FITS to PNG Conversion</p>
                        Before converting FITS to PNG, applying these scaling methods ensures that the resulting images retain
                        critical astronomical features and details that might otherwise be lost or obscured in the raw data. This
                        preprocessing step is essential for producing images that are not only visually appealing but also scientifically
                        valuable.
                    </p>
                </div>
            </div>
    )
}
export default ScalingInfo
