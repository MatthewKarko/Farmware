import * as React from 'react';
import { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Header from '../components/Header';
import { Switch } from '@mui/material';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axiosInstance from '../axios';
import { useNavigate } from 'react-router-dom';

const theme = createTheme();

export default function SignUp() {
  const [checked, setChecked] = useState(false);
  const navigate = useNavigate();

  const handleChange = (event) => {
    setChecked(event.target.checked);
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    
    var postObject = {
      first_name: data.get('firstName'),
      last_name: data.get('lastName'),
      email: data.get('email'),
      password: data.get('password')
    } 

    
    if(checked == true){
      
      postObject["org_name"] = data.get('org_name');
      axiosInstance.post(`user/register/admin/`, postObject).then((res)=>{
        navigate('/login')
        console.log(res)
        console.log(res.data)
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data != null && err.response.data.email != null){
          alert(err.response.data.email )
        }
        else if(err.response.data != null && err.response.data.detail != null){
          alert(err.response.data.detail);
        }
        else if(err.response.data != null && err.response.data.org_code != null){
          alert(err.response.data.org_code);
        } 
        else if(err.response.data != null && err.response.data.password != null){
          alert(err.response.data.password);
        } 
        else if(err.response.data != null ){
          alert(err.response.data);
        } 
      })
    }else{
      postObject["org_code"] = data.get('org_code');
      axiosInstance
        .post(`user/register/user/`, postObject)
        .then((res)=>{
          navigate('/login')
          console.log(res)
          console.log(res.data)
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data != null && err.response.data.email != null){
            alert(err.response.data.email )
          }
          else if(err.response.data != null && err.response.data.detail != null){
            alert(err.response.data.detail);
          } 
          else if(err.response.data != null && err.response.data.org_code != null){
            alert(err.response.data.org_code);
          } 
          else if(err.response.data != null && err.response.data.password != null){
            alert(err.response.data.password);
          } 
          else if(err.response.data != null ){
            alert(err.response.data);
          } 
          
        })
    }
    
   
    
  };

  return (
    <React.Fragment>

      <Header />
      <ThemeProvider theme={theme}>
        <Container component="main" maxWidth="xs">
          
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign up
            </Typography>
            <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
              <Grid container spacing={2}>
                <Grid item xs={12} >
                  <FormControlLabel
                  control={<Switch value="remember" color="primary" checked={checked} onChange={handleChange} />}
                  label="Sign up as admin"
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete="given-name"
                    name="firstName"
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    autoFocus
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    name="lastName"
                    autoComplete="family-name"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="new-password"
                  />
                </Grid>

                {checked ? (
                  <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="org_name"
                    label="Organisation Name"
                    type="org_name"
                    id="org_name"
                    autoComplete="org_name"
                  />
                </Grid>
                
                ) : 
                
                
                (
                  <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="org_code"
                    label="Organisation Code"
                    type="org_code"
                    id="org_code"
                    autoComplete="org_code"
                  />
                </Grid>
                  
                )}
                
                
              </Grid>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign Up
              </Button>
              <Grid container justifyContent="center" alignItems="center">
                <Grid item >
                  <Link href="/login" variant="body2" >
                    Already have an account? Sign in
                  </Link>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </Container>
      </ThemeProvider>
    </React.Fragment>
  );
}
