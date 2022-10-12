import React, { Component } from 'react';
import Navbar from '../components/Navbar';
import UsersTable from '../components/UserTableComponents/UsersTable';
import '../css/DashboardPages.css';
import Header from '../components/Header';
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Redirect
} from "react-router-dom";

export default function UsersTablePage() {

    return (
        <div className='mainContainer'>
            <Navbar />
            <div className='componentContainer'>
                <Header />
                <UsersTable />
            </div>
        </div>
    );
}