import React from 'react';
import { BrowserRouter as Router, Route, Redirect, Switch, Link } from 'react-router-dom';
import { AppBar, Tabs, Tab, Button, useMediaQuery, useTheme, IconButton } from '@mui/material';
import { Toolbar } from '@mui/material';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
import { makeStyles } from '@mui/material';
import LoginPage from '../webpages/LoginPage';
import DrawerComp from './DrawerComp';
import AgricultureIcon from '@mui/icons-material/Agriculture';

const PAGES = ["Login", "Signup"];

const Header = () => {
    const theme = useTheme();
    const isMatch = useMediaQuery(theme.breakpoints.down('md'));



    return(
        <React.Fragment>
            <AppBar
                position="static"
                sx={{background: "#026946"}}
            >
                <Toolbar>
                <IconButton href="/" sx={{color: 'white'}}>
                                    <AgricultureIcon
                                    sx={{marginRight: '15px'}}
                                    />
                </IconButton>
                <Typography variant="h6" color="inherit" noWrap  sx={{flexGrow: 1}}>
                            Farmware
                </Typography>
                    
                    {
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
                    }

                    
                </Toolbar>
        
            </AppBar>
        </React.Fragment>
    );
};

export default Header;