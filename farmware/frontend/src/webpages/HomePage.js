import React, {Component} from 'react';
import '../css/HomePage.css';
import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";

export default function HomePage() {
    return (
        <div className="App">
      <header className="App-header">
        <br></br>
        <br></br>
        <br></br>
        <h1>this is the home page when no user is logged in.</h1>
      </header>
    </div>
    );
}