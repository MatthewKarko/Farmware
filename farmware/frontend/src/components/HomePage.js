import React, {Component} from 'react';

import LoginPage from "./LoginPage";
import SignUpPage from "./SignUpPage";

import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";

export default class HomePage extends Component {
    constructor(props) {
        super(props);
    } 

    render() {
        // return <p>hello</p>;
        return (<Router>
        <Routes>
            <Route path='/' element={<p>hi</p>}/>
            <Route path="/login" element={<LoginPage />} />
        </Routes>
    </Router>);
    }
}