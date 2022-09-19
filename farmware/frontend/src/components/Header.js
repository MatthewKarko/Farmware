import React from 'react';
import { AppBar } from '@mui/material';
import { Toolbar } from '@mui/material';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
import { makeStyles } from '@mui/material';


const Header = () => {

    return(
        <React.Fragment>
            <AppBar
                position="static"
                
            >
                <Toolbar>
                    <Typography variant="h6" color="inherit" noWrap>
                        Farmware
                    </Typography>
                </Toolbar>

            </AppBar>
        </React.Fragment>
    );
};

export default Header;