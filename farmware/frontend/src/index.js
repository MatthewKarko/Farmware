import React from "react";
import { render } from "react-dom";
import App from "./App";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import LoginPage from "./webpages/LoginPage";
import SignUpPage from "./webpages/SignUpPage";
import GlobalContextProvider from "./context/GlobalContextProvider";
const routing = (
        <GlobalContextProvider>
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<App />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignUpPage />}/>
            </Routes>
            {/* <Footer /> */}
        </Router>
        </GlobalContextProvider>
 
    
    
);

render(routing, document.getElementById('app'))