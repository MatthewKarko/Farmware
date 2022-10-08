import React from "react";
import { render } from "react-dom";
import HomePage from "./webpages/HomePage";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import LoginPage from "./webpages/LoginPage";
import SignUpPage from "./webpages/SignUpPage";
import DashboardPage from "./webpages/DashboardPage";
import AccountSettingsPage from "./webpages/AccountSettingsPage";
import UsersTablePage from "./webpages/UsersTablePage";
import OrderPage from "./webpages/OrderPage";

const routing = (
    <Router>
        <Header />
        <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignUpPage />}/>
            <Route path="/dashboard" element={<DashboardPage />}/>
            <Route path="/accountsettings" element={<AccountSettingsPage />}/>
            <Route path="/userstable" element={<UsersTablePage />}/>
            <Route path="/order" element={<OrderPage />}/>
        </Routes>
        <Footer />
    </Router>
);

render(routing, document.getElementById('app'))