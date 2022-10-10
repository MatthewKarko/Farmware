import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import DashboardWidgets from '../components/DashboardComponents/DashboardWidgets';
import '../css/DashboardPages.css';
import axios from 'axios';
import axiosInstance from '../axios.js';
import Button from '@mui/material/Button';

import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";
import Header from '../components/Header';

export default function DashboardPage() {
    return (
        <div className='mainContainer'>
            <Navbar/> 
            <div className='componentContainer'>
            <Header/>
            <DashboardWidgets/>
            </div>
            
        </div>
  
    );
}