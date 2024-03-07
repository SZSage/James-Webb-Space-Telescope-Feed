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
        "https://i.pinimg.com/originals/e9/c9/2f/e9c92f7869d682a6fa5a97fb8a298f30.jpg"
    },
    {
      id: "3",
      instrument: "asset/writing.png",
      title: "Branding",
      desc:
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
      img:
        "https://i.pinimg.com/originals/a9/f6/94/a9f69465d972a004ad581f245d6ad581.jpg"
    }
  ];
  /*const images = [slides.map()]*/
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
