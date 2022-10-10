import React, { useState } from 'react'
import { Link } from "react-router-dom";
import '../css/Navbar.css';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import Inventory2Icon from '@mui/icons-material/Inventory2';
import DashboardIcon from '@mui/icons-material/Dashboard';
import DescriptionIcon from '@mui/icons-material/Description';
import PersonIcon from '@mui/icons-material/Person';
import GroupIcon from '@mui/icons-material/Group';
import EggIcon from '@mui/icons-material/Egg';
import SettingsIcon from '@mui/icons-material/Settings';

import logo from '../images/logo.jpg';
import { Container } from '@mui/system';

const drawerWidth = 240;

function Navbar() {
    return (
        <div className='navbar'>
            <Box>
                <Drawer
                    sx={{
                        width: drawerWidth,
                        flexShrink: 0,
                        '& .MuiDrawer-paper': {
                            width: drawerWidth,
                            boxSizing: 'border-box',
                        },
                    }}
                    variant="permanent"
                    anchor="left"
                >
                    <Container sx={{
                        width: drawerWidth,
                        alignItems: "center",
                        justifyContent: "center",
                        margin: "10px",
                    }}>
                        <img src={logo} alt="fireSpot" className='logoimage' />
                    </Container>


                    <List sx={{
                        margin: "10px",
                    }}>
                        <ListItem key="Dashboard" disablePadding>
                            <ListItemButton component={Link} to="/dashboard"  sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <DashboardIcon sx={{ color: "#000000" }} />
                                </ListItemIcon>
                                <ListItemText primary="Dashboard" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Orders" disablePadding>
                            <ListItemButton component={Link} to="/" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <InboxIcon sx={{ color: "#000000" }} />
                                </ListItemIcon>
                                <ListItemText primary="Orders" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Packaging" disablePadding>
                            <ListItemButton component={Link} to="/" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <Inventory2Icon sx={{ color: "#000000" }} />
                                </ListItemIcon>
                                <ListItemText primary="Packaging" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Stock" disablePadding>
                            <ListItemButton component={Link} to="/" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <DescriptionIcon sx={{ color: "#000000" }} />
                                </ListItemIcon>
                                <ListItemText primary="Stock" />
                            </ListItemButton>
                        </ListItem>
                    </List>
                    <Divider />
                    <List sx={{
                        margin: "10px",
                    }}>
                        <ListItem key="Account Settings" disablePadding>
                            <ListItemButton component={Link} to="/accountsettings"  sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <SettingsIcon sx={{ color: "#000000" }} />
                                </ListItemIcon>
                                <ListItemText primary="Account Settings" />
                            </ListItemButton>
                        </ListItem>
                    </List>

                    <Divider />

                    <List sx={{
                        margin: "10px",
                    }}>
                        <ListItem key="Users" disablePadding>
                            <ListItemButton component={Link} to="/userstable"  sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <PersonIcon sx={{ color: "#000000" }}/>
                                </ListItemIcon>
                                <ListItemText primary="Users" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Produce" disablePadding>
                            <ListItemButton component={Link} to="/"  sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <EggIcon sx={{ color: "#000000" }} />
                                </ListItemIcon>
                                <ListItemText primary="Produce" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Customers" disablePadding>
                            <ListItemButton component={Link} to="/"  sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <GroupIcon sx={{ color: "#000000" }} />
                                </ListItemIcon>
                                <ListItemText primary="Customers" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Packaging" disablePadding>
                            <ListItemButton component={Link} to="/"  sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <Inventory2Icon sx={{ color: "#000000" }}/>
                                </ListItemIcon>
                                <ListItemText primary="Packaging" />
                            </ListItemButton>
                        </ListItem>
                    </List>
                </Drawer>
            </Box>
        </div>
    )
}

export default Navbar