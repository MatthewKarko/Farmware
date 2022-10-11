import React from 'react';
import Navbar from '../components/Navbar';
import DashboardWidgets from '../components/DashboardComponents/DashboardWidgets';
import Header from '../components/Header';
import '../css/DashboardPages.css';

export default function DashboardPage() {
    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <div className='componentContainerContent'>
                    <DashboardWidgets />
                </div>
            </div>

        </div>

    );
}