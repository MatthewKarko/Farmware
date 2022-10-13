import React, { Component } from 'react';
import Navbar from '../components/Navbar';
import ProduceTable from '../components/tables/ProduceTable';
import '../css/DashboardPages.css';
import Header from '../components/Header';

export default function ProducePage() {

    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <ProduceTable />
            </div>
        </div>
    );
}