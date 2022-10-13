import React, { useState } from 'react';
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
import Avatar from '@mui/material/Avatar';
import DashboardIcon from '@mui/icons-material/Dashboard';

import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import Divider from '@mui/material/Divider';
import Settings from '@mui/icons-material/Settings';
import Logout from '@mui/icons-material/Logout';
import Box from '@mui/material/Box';
import Tooltip from '@mui/material/Tooltip';
import PersonAdd from '@mui/icons-material/PersonAdd';
const Header = () => {
    const theme = useTheme();
    const isMatch = useMediaQuery(theme.breakpoints.down('md'));
    const currentUser = localStorage.getItem('access_token');
    let navigate = useNavigate();

    const [anchorEl, setAnchorEl] = useState(false);


    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };
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
                    <React.Fragment>
                        <Box sx={{ display: 'flex', alignItems: 'center', textAlign: 'center', marginLeft: 'auto'}}>
                            <Tooltip title="Account settings">
                            <IconButton
                                onClick={handleClick}
                                size="small"
                                sx={{ ml: 2 }}
                                aria-controls={open ? 'account-menu' : undefined}
                                aria-haspopup="true"
                                aria-expanded={open ? 'true' : undefined}
                            >
                                <Avatar sx={{ width: 32, height: 32 }}>M</Avatar>
                            </IconButton>
                            </Tooltip>
                        </Box>
                        <Menu
                            anchorEl={anchorEl}
                            id="account-menu"
                            open={open}
                            onClose={handleClose}
                            onClick={handleClose}
                            PaperProps={{
                            elevation: 0,
                            sx: {
                                overflow: 'visible',
                                filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                                mt: 1.5,
                                '& .MuiAvatar-root': {
                                width: 32,
                                height: 32,
                                ml: -0.5,
                                mr: 1,
                                },
                                '&:before': {
                                content: '""',
                                display: 'block',
                                position: 'absolute',
                                top: 0,
                                right: 14,
                                width: 10,
                                height: 10,
                                bgcolor: 'background.paper',
                                transform: 'translateY(-50%) rotate(45deg)',
                                zIndex: 0,
                                },
                            },
                            }}
                            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                            >
                            <MenuItem component={Link} to='/accountsettings'>
                            <Avatar  sx={{ width: 10, height: 10 }} /> 
                            Profile
                            </MenuItem>
                            <MenuItem component={Link} to='/logout'>
                            <ListItemIcon>
                                <Logout fontSize="small" />
                            </ListItemIcon>
                            Logout
                            </MenuItem>
                        </Menu>
                    </React.Fragment>


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