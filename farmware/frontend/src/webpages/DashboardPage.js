import React, {useEffect} from 'react';
import { useNavigate } from "react-router-dom";
import Navbar from '../components/Navbar';
import DashboardWidgets from '../components/DashboardComponents/DashboardWidgets';
import '../css/DashboardPages.css';
import axios from 'axios';
import axiosInstance from '../axios.js';
import Button from '@mui/material/Button';
import {  } from 'react';

import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";
import Header from '../components/Header';

export default function DashboardPage() {
    let navigate = useNavigate();
    const currentUser = localStorage.getItem('access_token');
    useEffect(() => {
        if (!currentUser){
           return navigate("/login");
        }
     },[currentUser]);


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