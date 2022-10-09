import React, {Component} from 'react';
import { version } from 'react';

import '../css/HomePage.css';
import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";
import Header from '../components/Header';

export default function HomePage() {
  console.log(version);

    return (
      <React.Fragment>
        <Header />
        <header className="App-header">
          <br></br>
          <br></br>
          <br></br>
          <h1>this is the home page when no user is logged in.</h1>
        </header>
      </React.Fragment>
 
    );
}