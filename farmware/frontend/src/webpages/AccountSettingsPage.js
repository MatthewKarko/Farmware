import React, { Component } from 'react';
import Navbar from '../components/Navbar';
import AccountModify from '../components/AccountModify';
import '../css/DashboardPages.css';
import Header from '../components/Header';
import { SnackbarProvider } from 'notistack';

export default function AccountSettingsPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <AccountModify />
                </SnackbarProvider>
            </div>

        </div>
    );
}