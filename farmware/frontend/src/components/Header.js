import React from 'react';
import { BrowserRouter as Router, Route, Redirect, Switch, Link, useNavigate } from 'react-router-dom';
import axiosInstance from '../axios';
import { AppBar, Tabs, Tab, Button, useMediaQuery, useTheme, IconButton } from '@mui/material';
import { Toolbar } from '@mui/material';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
import { makeStyles } from '@mui/material';
import LoginPage from '../webpages/LoginPage';
import DrawerComp from './DrawerComp';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import DashboardIcon from '@mui/icons-material/Dashboard';

const Header = () => {
    const theme = useTheme();
    const isMatch = useMediaQuery(theme.breakpoints.down('md'));
    const currentUser = localStorage.getItem('access_token');
    let navigate = useNavigate();

    const logout = () => {
        console.log("here");
        axiosInstance.post('user/logout/blacklist/', {
			refresh_token: localStorage.getItem('refresh_token'),
		});
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		axiosInstance.defaults.headers['Authorization'] = null;
		navigate('/login');
    }

    return(
        <React.Fragment>
            
            <AppBar
                position="sticky"
                display="flex"
                sx={{background: "#026946"}}
            >
                <Toolbar>
                

                {!currentUser ? (
                    <>
                        <IconButton href="/" sx={{color: 'white'}}>
                                    <AgricultureIcon
                                    sx={{marginRight: '15px'}}
                                    />
                        </IconButton>
                        <Typography variant="h6" color="inherit" noWrap  sx={{flexGrow: 1}}>
                                    Farmware
                        </Typography>
                        <Button sx={{marginLeft: 'auto'}} variant='contained' href='/login'>  
                            Login
                        </Button>
                        <Button sx={{marginLeft: 'auto'}} variant='contained' href='/signup'>  
                            Signup
                        </Button>
                    </>

                ) : (
                    <>
                        <Button sx={{marginLeft: 'auto'}} variant='contained' href='/logout'>  
                            Logout
                        </Button>
                    </>


                    )}
                    
                    {/* {
                        isMatch ? (
                            <>
                            <DrawerComp />
                            </>
                        ) : (
                            <>
                                
                               
                            
                            
                            {
                                PAGES.map((page) => (
                            
                                    <Button sx={{marginLeft: 'auto'}} variant='contained' href={`/${page.toLowerCase()}`}>  
                                    {page}
                                    </Button>
                                ))   
                            }
                            </>
                        )
                    } */}

                    
                </Toolbar>
        
            </AppBar>
        </React.Fragment>
    );
};

export default Header;