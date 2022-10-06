import React, {Component} from 'react';
import Navbar from '../components/Navbar';
import '../css/DashboardPage.css';
import axios from 'axios';
import axiosInstance from '../axios.js';
import Button from '@mui/material/Button';

import { 
    BrowserRouter as Router, 
    Routes, 
    Route, 
    Link, 
    Redirect
} from "react-router-dom";

export default function DashboardPage() {
    const handleSubmit = (e) => {
		e.preventDefault();
		axiosInstance
			.get(`teams`, {
				// org_code:'000000',
                // org_name:'luke test org name',
                // organisation:'test organisation',
			})
			.then((res) => {
                console.log(res.data);
				// history.push('');
			});
	};

    return (
        <React.Fragment>
            <Navbar/> 
                <div className="offset" >
                    <br></br>
                    <h1> Dashboard page components here. </h1>
                    <h1> User reaches this page when they are logged in. </h1>

                    <Button
						type="submit"
						// className={classes.submit}
						// onClick={handleSubmit}
						onClick={handleSubmit}
					>
						Request teams (written to console.log)
					</Button>
                </div>
            </React.Fragment>
    );
}