import React, { Component } from 'react';
import Navbar from '../components/Navbar';
import '../css/DashboardPages.css';
import Header from '../components/Header';
import ProduceTable from '../components/tables/ProduceTable';

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