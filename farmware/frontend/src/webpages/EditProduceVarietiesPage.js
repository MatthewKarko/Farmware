import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import '../css/DashboardPages.css';
import Header from '../components/Header';
import { SnackbarProvider } from 'notistack';
import { EditProduceVarieties } from '../components/ProduceComponents/EditProduceVarieties';

export default function EditProduceVarietiesPage() {
    return (
        <div className='mainContainer'>
            <Navbar/> 
            <div className='componentContainer'>
                <Header />
                <SnackbarProvider maxSnack={3}>
                    <EditProduceVarieties />
                </SnackbarProvider>
            </div>
   
        </div>
    );
}