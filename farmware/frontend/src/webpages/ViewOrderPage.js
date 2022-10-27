import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import ViewOrder from '../components/orderComponents/ViewOrder';
import '../css/DashboardPages.css';
import Header from '../components/Header';
import { SnackbarProvider } from 'notistack';

export default function ViewOrderPage() {
    return (
        <div className='mainContainer'>
            <Navbar/> 
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <ViewOrder />
                </SnackbarProvider>
            </div>
   
        </div>
    );
}