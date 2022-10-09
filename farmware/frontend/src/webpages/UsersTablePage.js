import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import UsersTable from '../components/UserTableComponents/UsersTable';

import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";

export default function UsersTablePage() {

    return (
        <>
            <Navbar/> 
            <UsersTable/>
        </>
    );
}