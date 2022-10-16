import React from 'react';
import Navbar from '../components/Navbar';
import SuppliersTable from '../components/tables/SuppliersTable';
import Header from '../components/Header';
import '../css/DashboardPages.css';

export default function SuppliersPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <SuppliersTable />
            </div>
        </div>
    );
}