import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import OrderTable from '../components/OrdersComponents/OrderTable';
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

export default function OrderPage() {
    return (
        <>
            <Navbar/> 
            <OrderTable/>
        </>
    );
}