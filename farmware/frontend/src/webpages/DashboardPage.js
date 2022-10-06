import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import '../css/DashboardPage.css';
import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";


export default function DashboardPage() {
    return (
        <React.Fragment>
            <Navbar/> 
                <div className="offset" >
                    <br></br>
                    <h1> Dashboard page components here. </h1>
                    <h1> User reaches this page when they are logged in. </h1>
                </div>
            </React.Fragment>
    );
}