import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import AccountModify from '../components/AccountModify';
import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";

export default function AccountSettingsPage() {
    return (
        <>
            <Navbar/> 
            <AccountModify/>
        </>
    );
}