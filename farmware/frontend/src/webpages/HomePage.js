import React, { Component } from 'react';
import { useNavigate } from 'react-router-dom';
import { version } from 'react';
import { Button, Typography, Grid, Box } from '@mui/material';
import '../css/HomePage.css';
import Header from '../components/Header';
import logoFarmware from '../images/logo transparent.png';
import { createTheme, ThemeProvider } from '@mui/material/styles';

export default function HomePage() {
  const navigate = useNavigate();

  const theme = createTheme({
    palette: {
      primary: {
        main: '#028357',
      },
      secondary: {
        main: '#ffffff',
      },
    },
  });

  return (
    // If i make the fonts smaller, they might fit in the centre of the page when the margins are added to each
    <React.Fragment>
      <Header />
      <div className='main'>
        <Box sx={{ width: '100%', height: '100%' }}>
          <Grid container rowSpacing={0} columnSpacing={{ xs: 1, sm: 2, md: 4 }}
            alignItems="center"
            justifyContent="center"
            style={{ minHeight: '60vh' }}>

            <Grid item xs={4}>
              <Typography align="center" variant='h4' sx={{
                fontFamily: 'Lato',
                paddingBottom: '15px',
                fontWeight: 'bold'
              }}>Welcome to Farmware</Typography>
              <Typography align="center" variant='h7' sx={{
                fontFamily: 'Lato',
                paddingBottom: '20px',
                fontStyle: 'italic'
              }}>Farmware services the need for a digitised regulatory compliance aid—it provides an interface for farm admins and workers to collect and manage the required data for Freshcare standards.</Typography>
               
               <Typography align="center" variant='h7' sx={{
                fontFamily: 'Lato',
                margin: '10px',
                fontStyle: 'italic'
              }}> Farmware can leverage this data to power business intelligence and provide deep insight into the farm’s practices to assist decisions.</Typography>
              
              <ThemeProvider theme={theme}>
                <Box textAlign="center" sx={{
                  paddingTop: '15px'
                }}><Button variant="outlined" size="large" color="secondary"
                  style={{
                    backgroundColor: "#028357",
                  }}
                  onClick={() => navigate("/signup")}>Get Started</Button></Box>
              </ThemeProvider>
            </Grid>

            <Grid item xs={4}>
              <img src={logoFarmware} alt="temp" className='homelogoimage' />
            </Grid>

          </Grid>
        </Box>
      </div>
    </React.Fragment>
  );
}