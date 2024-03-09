import AwesomeSlider from "react-awesome-slider";
import "react-awesome-slider/dist/styles.css";
import slides from "./pics.json"
import './test.css';

export default function App() {
  const data = [
    {
      id: "1",
      instrument: "Infared lens",
      title: "Carina Nebula",
      desc:
        "This is the Carina Nebula pciture Taken by the James Webb Telescope",
      img:
        "carinanebula3.jpg"
    },
    {
      id: "2",
      instrument: "asset/globe.png",
      title: "Mobile Application",
      desc:
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
      img:
        "test-img.png"
    },
    {
      id: "3",
      instrument: "asset/writing.png",
      title: "Branding",
      desc:
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
      img:
        "CWEBTILE-2-5.png"
    }
  ];

  const dataNew =
  {
    "IR08572-NW_NIRCam_2024-03-08": {
        "target_name": "IR08572-NW",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F356W",
        "obs_title": "A JWST Survey of Ultraluminous Infrared Galaxies",
        "parent_obsid": "212641177",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Infrared galaxies, Interacting galaxies",
        "file_name": "jw03368-o111_t005_nircam_clear-f356w_i2d.fits",
        "start_time": "2024-03-08 06:19:13.557",
        "end_time": "2024-03-08 06:40:31.273",
        "exposure_time": "0:09:39.789000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw03368-o111_t005_nircam_clear-f356w_i2d.fits",
        "size": 150076800
    },
    "IR05189_NIRCam_2024-02-19": {
        "target_name": "IR05189",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F277W",
        "obs_title": "A JWST Survey of Ultraluminous Infrared Galaxies",
        "parent_obsid": "212511801",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Infrared galaxies, Interacting galaxies",
        "file_name": "jw03368-o106_t001_nircam_clear-f277w_i2d.fits",
        "start_time": "2024-02-19 04:18:57.523",
        "end_time": "2024-02-19 04:40:04.487",
        "exposure_time": "0:09:39.789000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw03368-o106_t001_nircam_clear-f277w_i2d.fits",
        "size": 150134400
    },
    "NGC1637_NIRCam_2024-02-05": {
        "target_name": "NGC1637",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F335M",
        "obs_title": "A JWST Census of the Local Galaxy Population: Anchoring the Physics of the Matter Cycle",
        "parent_obsid": "210094593",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Spiral galaxies",
        "file_name": "jw03707-o016_t009_nircam_clear-f335m_i2d.fits",
        "start_time": "2024-02-05 16:29:57.278",
        "end_time": "2024-02-05 16:40:52.230",
        "exposure_time": "0:06:26.524000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw03707-o016_t009_nircam_clear-f335m_i2d.fits",
        "size": 132111360
    },
    "URANUS_NIRCam_2024-02-06": {
        "target_name": "URANUS",
        "target_classification": "Solar System",
        "instrument_name": "NIRCam/image",
        "filters": "F460M",
        "obs_title": "JWST Cycle 1 Outreach Campaign",
        "parent_obsid": "173671567",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Planet",
        "file_name": "jw02739-o011_t002_nircam_clear-f460m_i2d.fits",
        "start_time": "2023-09-04 22:34:05.732",
        "end_time": "2023-09-05 00:15:33.525",
        "exposure_time": "0:30:25.250000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw02739-o011_t002_nircam_clear-f460m_i2d.fits",
        "size": 137859840
    },
    "NGC-4303-TILE-1_NIRCam_2024-02-06": {
        "target_name": "NGC-4303-TILE-1",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F360M",
        "obs_title": "A JWST-HST-VLT/MUSE-ALMA Treasury of Star Formation in Nearby Galaxies",
        "parent_obsid": "210371117",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Spiral galaxies",
        "file_name": "jw02107-o044_t020_nircam_clear-f360m_i2d.fits",
        "start_time": "2024-02-06 17:21:19.938",
        "end_time": "2024-02-06 17:42:26.918",
        "exposure_time": "0:07:09.472000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw02107-o044_t020_nircam_clear-f360m_i2d.fits",
        "size": 132128640
    },
    "URANUS_NIRCam_2024-02-07": {
        "target_name": "URANUS",
        "target_classification": "Solar System",
        "instrument_name": "NIRCam/image",
        "filters": "F460M",
        "obs_title": "JWST Cycle 1 Outreach Campaign",
        "parent_obsid": "173671567",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Planet",
        "file_name": "jw02739-o011_t002_nircam_clear-f460m_i2d.fits",
        "start_time": "2023-09-04 22:34:05.732",
        "end_time": "2023-09-05 00:15:33.525",
        "exposure_time": "0:30:25.250000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw02739-o011_t002_nircam_clear-f460m_i2d.fits",
        "size": 137859840
    },
    "NGC2283_NIRCam_2024-02-08": {
        "target_name": "NGC2283",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F300M",
        "obs_title": "A JWST Census of the Local Galaxy Population: Anchoring the Physics of the Matter Cycle",
        "parent_obsid": "210675880",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Spiral galaxies",
        "file_name": "jw03707-o024_t014_nircam_clear-f300m_i2d.fits",
        "start_time": "2024-02-08 12:43:11.693",
        "end_time": "2024-02-08 12:51:14.866",
        "exposure_time": "0:03:34.736000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw03707-o024_t014_nircam_clear-f300m_i2d.fits",
        "size": 132111360
    },
    "HUDF-DEEP-F160W_NIRISS_2024-01-30": {
        "target_name": "HUDF-DEEP-F160W",
        "target_classification": "Galaxy",
        "instrument_name": "NIRISS/image",
        "filters": "CLEAR;F200W",
        "obs_title": "The Next Generation Deep Extragalactic Exploratory Public (NGDEEP) Survey: Feedback in Low-Mass Galaxies from Cosmic Dawn to Dusk",
        "parent_obsid": "113644309",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Emission line galaxies, High-redshift galaxies, Lyman-alpha galaxies, Lyman-break galaxies",
        "file_name": "jw02079-o004_t001_niriss_clear-f200w_i2d.fits",
        "start_time": "2023-02-01 15:44:31.167",
        "end_time": "2023-02-02 01:21:37.554",
        "exposure_time": "0:28:37.880000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw02079-o004_t001_niriss_clear-f200w_i2d.fits",
        "size": 138075840
    },
    "HUDF-DEEP-F160W_NIRISS_2024-02-01": {
        "target_name": "HUDF-DEEP-F160W",
        "target_classification": "Galaxy",
        "instrument_name": "NIRISS/image",
        "filters": "CLEAR;F200W",
        "obs_title": "The Next Generation Deep Extragalactic Exploratory Public (NGDEEP) Survey: Feedback in Low-Mass Galaxies from Cosmic Dawn to Dusk",
        "parent_obsid": "113644309",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Emission line galaxies, High-redshift galaxies, Lyman-alpha galaxies, Lyman-break galaxies",
        "file_name": "jw02079-o004_t001_niriss_clear-f200w_i2d.fits",
        "start_time": "2023-02-01 15:44:31.167",
        "end_time": "2023-02-02 01:21:37.554",
        "exposure_time": "0:28:37.880000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw02079-o004_t001_niriss_clear-f200w_i2d.fits",
        "size": 138075840
    },
    "HUDF-DEEP-F160W_NIRISS_2024-01-23": {
        "target_name": "HUDF-DEEP-F160W",
        "target_classification": "Galaxy",
        "instrument_name": "NIRISS/image",
        "filters": "CLEAR;F200W",
        "obs_title": "The Next Generation Deep Extragalactic Exploratory Public (NGDEEP) Survey: Feedback in Low-Mass Galaxies from Cosmic Dawn to Dusk",
        "parent_obsid": "113644309",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Emission line galaxies, High-redshift galaxies, Lyman-alpha galaxies, Lyman-break galaxies",
        "file_name": "jw02079-o004_t001_niriss_clear-f200w_i2d.fits",
        "start_time": "2023-02-01 15:44:31.167",
        "end_time": "2023-02-02 01:21:37.554",
        "exposure_time": "0:28:37.880000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw02079-o004_t001_niriss_clear-f200w_i2d.fits",
        "size": 138075840
    },
    "NGC1792_NIRCam_2024-01-17": {
        "target_name": "NGC1792",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F335M",
        "obs_title": "A JWST Census of the Local Galaxy Population: Anchoring the Physics of the Matter Cycle",
        "parent_obsid": "204349169",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Spiral galaxies",
        "file_name": "jw03707-o020_t011_nircam_clear-f335m_i2d.fits",
        "start_time": "2024-01-17 18:40:30.354",
        "end_time": "2024-01-17 18:51:25.305",
        "exposure_time": "0:06:26.524000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw03707-o020_t011_nircam_clear-f335m_i2d.fits",
        "size": 132050880
    },
    "NGC1068_NIRCam_2024-01-08": {
        "target_name": "NGC1068",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F335M",
        "obs_title": "A JWST Census of the Local Galaxy Population: Anchoring the Physics of the Matter Cycle",
        "parent_obsid": "200910703",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Spiral galaxies",
        "file_name": "jw03707-o128_t002_nircam_clear-f335m_i2d.fits",
        "start_time": "2024-01-08 04:30:13.231",
        "end_time": "2024-01-08 04:41:08.246",
        "exposure_time": "0:06:26.524000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw03707-o128_t002_nircam_clear-f335m_i2d.fits",
        "size": 132111360
    },
    "Requiem2_NIRCam_2024-01-08": {
        "target_name": "Requiem2",
        "target_classification": "Star",
        "instrument_name": "NIRCam/image",
        "filters": "F444W",
        "obs_title": "Lensed Supernova Encore at z=2! The First Galaxy to Host Two Multiply-Imaged Supernovae",
        "parent_obsid": "212634225",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Type Ia supernovae",
        "file_name": "jw06549-c1000_t001_nircam_clear-f444w_i2d.fits",
        "start_time": "2023-12-05 21:43:22.165",
        "end_time": "2023-12-23 20:10:29.226",
        "exposure_time": "0:48:40.404000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw06549-c1000_t001_nircam_clear-f444w_i2d.fits",
        "size": 173396160
    },
    "NGC1808_NIRCam_2024-01-09": {
        "target_name": "NGC1808",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F335M",
        "obs_title": "A JWST Census of the Local Galaxy Population: Anchoring the Physics of the Matter Cycle",
        "parent_obsid": "201206295",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Spiral galaxies",
        "file_name": "jw03707-o122_t012_nircam_clear-f335m_i2d.fits",
        "start_time": "2024-01-09 14:42:18.423",
        "end_time": "2024-01-09 14:53:13.374",
        "exposure_time": "0:06:26.524000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw03707-o122_t012_nircam_clear-f335m_i2d.fits",
        "size": 131990400
    },
    "MACSJ0416.1-2403_NIRISS_2024-01-09": {
        "target_name": "MACSJ0416.1-2403",
        "target_classification": "Clusters of Galaxies",
        "instrument_name": "NIRISS/image",
        "filters": "CLEAR;F115W",
        "obs_title": "CANUCS: The CAnadian NIRISS Unbiased Cluster Survey",
        "parent_obsid": "183624080",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Rich clusters",
        "file_name": "jw01208-o004_t002_niriss_clear-f115w_i2d.fits",
        "start_time": "2023-01-11 20:31:47.513",
        "end_time": "2023-01-12 00:42:55.092",
        "exposure_time": "0:22:54.308000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw01208-o004_t002_niriss_clear-f115w_i2d.fits",
        "size": 133983360
    },
    "NGC-4321_NIRCam_2024-01-10": {
        "target_name": "NGC-4321",
        "target_classification": "Galaxy",
        "instrument_name": "NIRCam/image",
        "filters": "F360M",
        "obs_title": "A JWST-HST-VLT/MUSE-ALMA Treasury of Star Formation in Nearby Galaxies",
        "parent_obsid": "109838029",
        "description": "exposure/target (L2b/L3): rectified 2D image",
        "keywords": "Spiral galaxies",
        "file_name": "jw02107-o032_t014_nircam_clear-f360m_i2d.fits",
        "start_time": "2023-01-17 10:50:25.669",
        "end_time": "2023-01-17 11:11:32.649",
        "exposure_time": "0:07:09.472000",
        "calib_level": 3,
        "fits_url": "mast:JWST/product/jw02107-o032_t014_nircam_clear-f360m_i2d.fits",
        "size": 132186240
    }
  }

  return (
    <>
    <div className="App">
      <AwesomeSlider>
        {data.map((d) => (
            <>
            <div className="item">
                <div className="right">
                    <img className="currentImage" src={d.img} alt="could not display figure"/>
                </div>
                <div className="left">
                    <div className="leftContainer">
                        <h2>{d.title}</h2>
                        <p>Description: {d.desc} </p>
                        <p>Instrument: {d.instrument}</p>
                    </div>
                </div>
            </div>
          </>
        ))}
      </AwesomeSlider>
    </div>
    </>
  );
}