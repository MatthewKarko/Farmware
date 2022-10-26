import React from 'react';
import Navbar from '../components/Navbar';
import CustomersTable from '../components/tables/CustomersTable';
import Header from '../components/Header';
import '../css/DashboardPages.css';
import { SnackbarProvider } from 'notistack';

export default function CustomerPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <CustomersTable />
                </SnackbarProvider>
            </div>
        </div>
    );
}