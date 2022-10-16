import React from 'react';
import Navbar from '../components/Navbar';
import TeamsTable from '../components/tables/TeamsTable';
import Header from '../components/Header';
import '../css/DashboardPages.css';

export default function SuppliersPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <TeamsTable />
            </div>
        </div>
    );
}