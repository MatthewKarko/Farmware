import React from 'react';
import Navbar from '../components/Navbar';
import TeamsTable from '../components/tables/TeamsTable';
import Header from '../components/Header';
import '../css/DashboardPages.css';
import { SnackbarProvider } from 'notistack';

export default function SuppliersPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <TeamsTable />
                </SnackbarProvider>
            </div>
        </div>
    );
}