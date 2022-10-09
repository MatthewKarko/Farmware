import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import DashboardWidgets from '../components/DashboardComponents/DashboardWidgets';
import '../css/DashboardPage.css';
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

export default function DashboardPage() {
    return (
        <>
            <Navbar/> 
            <DashboardWidgets/>
        </>
    );
}