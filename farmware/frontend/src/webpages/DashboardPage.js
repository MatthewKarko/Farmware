import React, { useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import Navbar from '../components/Navbar';
import DashboardWidgets from '../components/DashboardComponents/DashboardWidgets';
import '../css/DashboardPages.css';
import Header from '../components/Header';

export default function DashboardPage() {
    let navigate = useNavigate();
    const currentUser = localStorage.getItem('access_token');
    useEffect(() => {
        if (!currentUser) {
            return navigate("/login");
        }
    }, [currentUser]);


    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <div className='componentMain'>
                    <DashboardWidgets />
                </div>
            </div>
        </div>
    );
}