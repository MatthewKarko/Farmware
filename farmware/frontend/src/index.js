import React from "react";
import { render } from "react-dom";
import HomePage from "./webpages/HomePage";
import { Route, BrowserRouter as Router, Routes, useNavigate, Navigate } from "react-router-dom";

import LoginPage from "./webpages/LoginPage";
import SignUpPage from "./webpages/SignUpPage";
import DashboardPage from "./webpages/DashboardPage";
import AccountSettingsPage from "./webpages/AccountSettingsPage";
import UsersTablePage from "./webpages/UsersTablePage";
import OrderPage from "./webpages/OrderPage";
import Logout from "./components/Logout";
import ProducePage from "./webpages/ProducePage";
import CustomersPage from "./webpages/CustomersPage";

const routing = (
    <Router>
        <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignUpPage />}/>
            <Route path="/logout" element={<Logout />}/>
            <Route path="/dashboard" element={<DashboardPage />}/>
            <Route path="/accountsettings" element={<AccountSettingsPage />}/>
            <Route path="/userstable" element={<UsersTablePage />}/>
            <Route path="/order" element={<OrderPage />}/>
            <Route path="/produce" element={<ProducePage />}/>
            <Route path="/customers" element={<CustomersPage />}/>

        </Routes>
    </Router>
);

render(routing, document.getElementById('app'))