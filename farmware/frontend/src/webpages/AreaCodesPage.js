import React from 'react';
import Navbar from '../components/Navbar';
import AreaCodesTable from '../components/tables/AreaCodesTable';
import Header from '../components/Header';
import '../css/DashboardPages.css';

export default function AreaCodesPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <AreaCodesTable />
            </div>
        </div>
    );
}