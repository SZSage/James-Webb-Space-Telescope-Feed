import AwesomeSlider from "react-awesome-slider";
import React from "react";
import "react-awesome-slider/dist/styles.css";
import './test.css';
import { Carousel } from "react-responsive-carousel";
import "react-responsive-carousel/lib/styles/carousel.min.css";
import datav5 from './exportJSON.js';
import datav7 from './testJSON.js';


export default function App() {
  let sourceP = "./processed_png/";
  let tag = ".png";


 const modifiedJSON = Object.keys(datav5).reduce((acc, key) => {
  const filePath = key;
  acc[key] = {
      ...datav5[key],
      new_path: filePath
  };
  return acc;
}, {});

console.log(modifiedJSON);


const arrayOfObjects = Object.values(modifiedJSON);


const datafileName = arrayOfObjects.map((d) => {
  const updatedFilename = sourceP + d.new_path + tag;
  return {
    ...d,
    new_path: updatedFilename
  }
 });

console.log(datafileName);

  return (
    <>
    <div className="App">
      <AwesomeSlider>
        {datafileName.map((d) => (
            <>
            <div className="item">
                <div className="right">
                    <img className="currentImage" src={d.new_path} alt="could not display figure"/>
                </div>
                <div className="left">
                    <div className="leftContainer">
                        <h2>Date: {d.start_time}</h2>
                        <h2 className="title-target">{d.obs_title} </h2>
                        <h2 className="title-target">Target Name: {d.target_name}</h2>
                        <p>Clasification: {d.target_classification} {d.keywords}</p>
                        <p>Instrument: {d.instrument_name}</p>
                        <p>Filters: {d.filters} </p>
                        <p>End Time: {d.end_time}</p>
                        <p>Total Exposure Time: {d.exposure_time}  ( hh : mm : ss.ms )</p>
                        <p>Calibration Level: {d.calib_level}</p>
                    </div>
                    <p className="desc2" >Description: {d.description}</p>
                    <p>Keywords: {d.keywords}</p>
                    <p>FIT file: {d.file_name}</p>
                    <p>FIT URL: {d.fits_url}</p>
                </div>
            </div>
          </>
        ))}
      </AwesomeSlider>
    </div>

    <div className="mobile-container">
    <Carousel useKeyboardArrows={true}>
        {datafileName.map((d, index) => (
            <>
          <div className="slide">
            <img alt="sample_file" src={d.new_path} key={index} />
          </div>
          <div className="slide-description">
                        <h2 className="title-target">{d.obs_title} </h2>
                        <h2 className="title-target">Target Name: {d.target_name}</h2>
                        <h2 className="date">Date: {d.start_time}</h2>
                        <p>Clasification: {d.target_classification} {d.keywords}</p>
                        <p>Instrument: {d.instrument_name}</p>
                        <p>Filters: {d.filters} </p>
                        <p>End Time: {d.end_time}</p>
                        <p>Total Exposure Time: {d.exposure_time}  ( hh : mm : ss.ms )</p>
                        <p>Calibration Level: {d.calib_level}</p>
                    <p className="desc2" >Description: {d.description}</p>
                    <p>Keywords: {d.keywords}</p>
                    <p>FIT file: {d.file_name}</p>


          </div>
          </>
        ))}
      </Carousel>
    </div>
    </>
  );
}
