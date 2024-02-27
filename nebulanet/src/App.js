import React, { Component } from 'react';
import NavBar from './components/NavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'
import Home from './components/pages/Home.js'
import About from './components/pages/About.js'


function App() {
  return (
    <>
    <Router>
      <NavBar/>
      <Routes>
        <Route path='/' exact Component={Home}/>
        <Route path='/about' exact Component={About}/>
      </Routes>
    </Router>
    </>
  );
}

export default App;
