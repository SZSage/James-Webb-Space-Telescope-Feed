import React, { Component } from 'react';
import NavBar from './components/NavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'
import Home from './components/pages/Home.js'
import About from './components/pages/About.js'
import Sources from './components/pages/Sources.js'
import Telescope from './components/pages/Telescope.js';
/*
App.js is the main js file that loads the website and redirects the user to the appropriate page when the user clicks a certian
link. It does that by utilizing the react-router-dom libary which was the easiest way for this feature to be accomplished and
it provides this functionality very well
*/


function App() {
  return (
    <>
    <Router>
      <NavBar/>
      <Routes>
        <Route path='/' exact Component={Home}/>
        <Route path='/about' exact Component={About}/>
        <Route path='/sources' exact Component={Sources}/>
        <Route path='/telescope' exact Component={Telescope}/>
      </Routes>
    </Router>
    </>
  );
}

export default App;
