import React, { Component } from 'react';
import Navbar from '../components/Navbar';
import UsersTable from '../components/tables/UsersTable';
import '../css/DashboardPages.css';
import Header from '../components/Header';
import { SnackbarProvider } from 'notistack';

export default function UsersTablePage() {

    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <UsersTable />
                </SnackbarProvider>
            </div>
        </div>
    );
}