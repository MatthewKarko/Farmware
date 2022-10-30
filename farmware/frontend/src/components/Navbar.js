import React, { useEffect, useState } from 'react'
import { Link } from "react-router-dom";
import { Box, Drawer, List, Typography, Divider, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { Container } from '@mui/system';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import Inventory2Icon from '@mui/icons-material/Inventory2';
import DashboardIcon from '@mui/icons-material/Dashboard';
import DescriptionIcon from '@mui/icons-material/Description';
import PersonIcon from '@mui/icons-material/Person';
import GroupIcon from '@mui/icons-material/Group';
import EggIcon from '@mui/icons-material/Egg';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import GroupsIcon from '@mui/icons-material/Groups';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import '../css/Navbar.css';
import axiosInstance from '../axios';

const drawerWidth = 240;

function Navbar() {
    const [orgCode, setOrganisationCode] = useState('');
    useEffect(() => {
        if(localStorage.getItem('organisation') != null){
            setOrganisationCode(localStorage.getItem('organisation'));
        }else{
            axiosInstance
            .get(`user/me/`)
            .then((res) => {
                localStorage.setItem('organisation', res.data.organisation);
                setOrganisationCode(localStorage.getItem('organisation'));
            })
        }
        
    }, [])
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
                    PaperProps={{
                        sx: {
                            backgroundColor: "#303030",
                        }
                    }}
                    variant="permanent"
                    anchor="left"
                >
                    <Container sx={{
                        width: 200,
                        justifyContent: "center",
                        paddingTop: "10px",
                        paddingLeft: "10px",
                        color: "#ffffff"
                    }}>
                        <Typography variant='h4' sx={{
                            fontFamily: 'Lato',
                            color: "#028357",
                            fontWeight: 'bold'
                        }}>Farmware</Typography>
                        <Typography variant='subtitle1' sx={{
                            fontFamily: 'Lato',
                            color: "#ffffff",
                            fontWeight: 'bold'
                        }}>Org Code: {orgCode}</Typography>
                    </Container>


                    <List sx={{
                        margin: "10px",
                        color: "#ffffff"
                    }}>
                        <ListItem key="Dashboard" disablePadding>
                            <ListItemButton component={Link} to="/dashboard" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <DashboardIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Dashboard" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Orders" disablePadding>
                            <ListItemButton component={Link} to="/orders" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <InboxIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Orders" />
                            </ListItemButton>
                        </ListItem>


                        <ListItem key="Stock" disablePadding>
                            <ListItemButton component={Link} to="/stock" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <DescriptionIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Stock" />
                            </ListItemButton>
                        </ListItem>
                    </List>
                    <Divider />

                    <List sx={{
                        margin: "10px",
                        color: "#ffffff"
                    }}>
                        <ListItem key="Users" disablePadding>
                            <ListItemButton component={Link} to="/userstable" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <PersonIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Users" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Produce" disablePadding>
                            <ListItemButton component={Link} to="/produce" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <EggIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Produce" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Customers" disablePadding>
                            <ListItemButton component={Link} to="/customers" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <GroupIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Customers" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Suppliers" disablePadding>
                            <ListItemButton component={Link} to="/suppliers" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <LocalShippingIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Suppliers" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Teams" disablePadding>
                            <ListItemButton component={Link} to="/teams" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <GroupsIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Teams" />
                            </ListItemButton>
                        </ListItem>

                        <ListItem key="Area Codes" disablePadding>
                            <ListItemButton component={Link} to="/area_codes" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <LocationOnIcon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Area Codes" />
                            </ListItemButton>
                        </ListItem>

                        {/* <ListItem key="Packaging" disablePadding>
                            <ListItemButton component={Link} to="/" sx={{
                                "&:hover": {
                                    backgroundColor: "#028357",
                                    borderRadius: "3px",
                                },
                            }}>
                                <ListItemIcon>
                                    <Inventory2Icon sx={{ color: "#ffffff" }} />
                                </ListItemIcon>
                                <ListItemText primary="Packaging" />
                            </ListItemButton>
                        </ListItem> */}
                    </List>
                </Drawer>
            </Box>
        </div>
    )
}

export default Navbar