import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import ViewOrder from '../components/orderComponents/ViewOrder';
import '../css/DashboardPages.css';
import Header from '../components/Header';

export default function ViewOrderPage() {
    return (
        <div className='mainContainer'>
            <Navbar/> 
            <div className='componentContainer'>
                <Header />
                <ViewOrder/>
            </div>
   
        </div>
    );
}