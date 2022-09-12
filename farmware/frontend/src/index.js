import React from "react";
import { render } from "react-dom";
import App from "./App";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
const routing = (
    <Router>
        <Header />
        <Routes>
            <Route path="/" element={<App />} />
        </Routes>
        <Footer />
    </Router>
    
    
);

render(routing, document.getElementById('app'))