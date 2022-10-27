import React from 'react';
import Navbar from '../components/Navbar';
import AreaCodesTable from '../components/tables/AreaCodesTable';
import Header from '../components/Header';
import '../css/DashboardPages.css';
import { SnackbarProvider } from 'notistack';

export default function AreaCodesPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <AreaCodesTable />
                </SnackbarProvider>
            </div>
        </div>
    );
}