import React, { Component } from 'react';
import Navbar from '../components/Navbar';
import '../css/DashboardPages.css';
import Header from '../components/Header';
import StockTable from '../components/tables/StockTable';
import { SnackbarProvider } from 'notistack';

export default function StockPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <StockTable />
                </SnackbarProvider>
            </div>
        </div>
    );
}