import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import AccountModify from '../components/AccountModify';
import '../css/DashboardPages.css';
import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";

export default function AccountSettingsPage() {
    return (
        <div className='mainContainer'>
            <Navbar/> 
            <div className='componentContainer'>
            <AccountModify/>
            </div>
            
        </div>
    );
}