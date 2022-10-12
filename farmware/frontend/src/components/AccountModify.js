import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormLabel from '@mui/material/FormLabel';
import Checkbox from '@mui/material/Checkbox';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import ListItemText from '@mui/material/ListItemText';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axiosInstance from '../axios';
import Header from '../components/Header';



const theme = createTheme();

export default function AccountModify() {
  let navigate = useNavigate();
  const [userObj, setUserObj] = useState([]);
  const [teamList, setTeamlist] = useState([]);
  const [currentTeam, setCurrentTeam] = useState('');

  useEffect(() => {
    axiosInstance
			.get(`user/me/`, {
			})
			.then((res) => {
				console.log(res.data);
        setUserObj(res.data);
				// console.log(res);
       
			})
      .catch((err) => {
        // console.log("AXIOS ERROR: ", err);
        alert("Incorrect creditials entered");
      });
    axiosInstance
		  .get(`teams/`, {
			})
			.then((res) => {
				
        res.data.map((data) => {
          // teamList.push(data.name);
          // console.log(data);
          setTeamlist(teamList => [...teamList, data])
          


        })
        

        
			})
      .catch((err) => {
        console.log("AXIOS ERROR: ", err);
        // alert("ERROR: Incorrect call");
    });
    
  }, []);

  const handleChange = (evt) => {
    const value = evt.target.value;
    setUserObj({
      ...userObj,
      [evt.target.name]: value
    });

  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    var postObject = {
        first_name: data.get('first_name'),
        last_name: data.get('last_name'),
        email: data.get('email')

       
      } 
      
      
      
     
      axiosInstance
        .patch(`user/${userObj.id}/`, postObject)
        .then((res)=>{
            console.log(res);
            alert("successfully changed account information");
            navigate('/dashboard');
            
        
      });


  };

  

  return (
    <React.Fragment>

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
            <Avatar sx={{ m: 1, bgcolor: 'green' }}>
              <AccountCircleIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Modify Account
            </Typography>
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
              <TextField 
                InputLabelProps={{ shrink: !! userObj.first_name }}
                onChange={handleChange}
                margin="normal"
                required
                fullWidth
                id="first_name"
                label="Firstname"
                name="first_name"
                autoComplete="first_name"
                value={userObj.first_name}
                autoFocus
              />
              <TextField
                InputLabelProps={{ shrink: !! userObj.last_name }}
                onChange={handleChange}
                value={userObj.last_name}
                margin="normal"
                required
                fullWidth
                id="last_name"
                label="Lastname"
                name="last_name"
                autoComplete="last_name"
                autoFocus
              />
              <TextField
                InputLabelProps={{ shrink: !! userObj.email }}
                onChange={handleChange}
                value={userObj.email}
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
              />
              <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Teams</InputLabel>
                  <Select
                    value={"Teams"}
                    label="Teams"
                    onChange={handleChange}
                  >
                   {/* <MenuItem key={1} value={1}>test</MenuItem> */}
                  {
                      // names = ['t1', 't2', 'TestTeam'];
                      teamList.map((team) => {
                 
                        return(
                        <MenuItem key={team.id} value={team.name}>{team.name}</MenuItem>
                        )
                      })
                  }
                  </Select>
              </FormControl>
              <FormLabel
              
                children="Enter password to confirm"
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
              />
              
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Submit Modifications
              </Button>
              <Grid container>
                <Grid item xs>
                  <Link href="#" variant="body2">
                    Forgot password?
                  </Link>
                </Grid>
                
              </Grid>
            </Box>
          </Box>
        </Container>

    </React.Fragment>
  );
}