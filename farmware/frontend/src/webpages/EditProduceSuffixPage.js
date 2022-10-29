import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import '../css/DashboardPages.css';
import Header from '../components/Header';
import { SnackbarProvider } from 'notistack';
import { EditProduceSuffix } from '../components/ProduceComponents/EditProduceSuffix';

export default function EditProduceSuffixPage() {
    return (
        <div className='mainContainer'>
            <Navbar/> 
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <EditProduceSuffix />
                </SnackbarProvider>
            </div>
   
        </div>
    );
}