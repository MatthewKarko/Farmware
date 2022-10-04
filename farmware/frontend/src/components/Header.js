import React from 'react';
import { BrowserRouter as Router, Route, Redirect, Switch, Link, useNavigate } from 'react-router-dom';
import { AppBar, Tabs, Tab, Button, useMediaQuery, useTheme, IconButton } from '@mui/material';
import { Toolbar } from '@mui/material';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
import { makeStyles } from '@mui/material';
import LoginPage from '../webpages/LoginPage';
import DrawerComp from './DrawerComp';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import { useValue } from '../context/GlobalContextProvider';

const Header = () => {
    const theme = useTheme();
    const isMatch = useMediaQuery(theme.breakpoints.down('md'));
    const {state:{currentUser, pages} , dispatch} = useValue();
    const navigate = useNavigate();
    console.log(currentUser)

    
    return(
        <React.Fragment>
            <AppBar
                position="static"
                sx={{background: "#026946"}}
            >
                <Toolbar>
                <IconButton sx={{color: 'white'}} href='/' >
                                    <AgricultureIcon
                                    sx={{marginRight: '15px'}}
                                    />

                </IconButton>
                <Typography variant="h6" color="inherit" noWrap  sx={{flexGrow: 1}}>
                            Farmware

                </Typography>
                    
                {!currentUser ? (
                    <>
                    <Button sx={{marginLeft: 'auto'}} variant='contained' href='/login'>  
                    Login
                    </Button>
                    <Button sx={{marginLeft: 'auto'}} variant='contained' href='/signup'>  
                    Signup
                    </Button>
                    </>

                ) : (
                    <>
                    <Button sx={{marginLeft: 'auto'}} variant='contained' o={console.log("pressed")}>  
                    Logout
                    </Button>
                    </>
                    
                    
                    )}
                    {/* {   

                        isMatch ? (
                            
                            <>
                            {!currentUser ? (console.log(pages)) : (console.log(pages))}
                            <DrawerComp />
                            </>
                        ) : (
                            
                            <>
                            
                            
                            {
                                
                                pages.map((page) => {
                                    if(page === "Logout"){
                                        return(
                                            <Button sx={{marginLeft: 'auto'}} variant='contained' onClick={console.log("logged out")}>  
                                            {page}
                                            </Button>
                                        )
                                        
                                    }else{
                                        return(
                                            <Button sx={{marginLeft: 'auto'}} variant='contained' href={`/${page.toLowerCase()}`}>  
                                            {page}
                                            </Button>
                                        )
                                    }
                                    
                                    
                                })   
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