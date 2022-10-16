import React from 'react';
import Navbar from '../components/Navbar';
import CustomersTable from '../components/tables/CustomersTable';
import Header from '../components/Header';
import '../css/DashboardPages.css';

export default function CustomerPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <CustomersTable />
            </div>
        </div>
    );
}