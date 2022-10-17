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
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';




const theme = createTheme();

export default function AccountModify() {
  let navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [userObj, setUserObj] = useState([]);
  const [teamList, setTeamlist] = useState([]);
  const [currentTeams, setCurrentTeams] = useState([]);
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');



  

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
    axiosInstance
		  .get(`user/teams/`, {
			})
			.then((res) => {
		
        
        res.data.teams.map((data) => {
          // teamList.push(data.name);
          // console.log(data);
          setCurrentTeams(currentTeams => [...currentTeams, data.name])
        })        
			})
      .catch((err) => {
        console.log("AXIOS ERROR: ", err);
        // alert("ERROR: Incorrect call");
    });



    
  }, []);

  const handleClickOpen = (event) => {
    event.preventDefault();
    setOpen(true);
  };

  const handleClose = (event) => {
    event.preventDefault();
    setOpen(false);
  };

  const handleChange = (evt) => {
    const value = evt.target.value;
    setUserObj({
      ...userObj,
      [evt.target.name]: value
    });

  }
  const handleOldPasswordChange = (evt) => {
    evt.preventDefault();
    const value = evt.target.value;
    setOldPassword(value);

  };
  const handleNewPasswordChange = (evt) => {
    evt.preventDefault();
    const value = evt.target.value;
    setNewPassword(value);

  }


  const handlePasswordSubmit = (event) => {
    event.preventDefault();
    // const data = new FormData(event.currentTarget);
    var postObject = {
      old_password: oldPassword,
      new_password: newPassword
    } 

    axiosInstance
        .post(`user/${userObj.id}/set_password/`, postObject)
        .then((res)=>{
            console.log(res);
            alert("Successfully changed account password");
            navigate('/dashboard');
        })
        .catch((err) => {
          
          alert(err.response.data.new_password);
        });
    
  };

  const handleTeamChange = (event) => {
    const {
      target: { value },
    } = event;
    setCurrentTeams(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    if(!confirm("Confirm account changes")){
      navigate('/accountsettings');
    }else{

      var postObject = {
        first_name: data.get('first_name'),
        last_name: data.get('last_name'),
        email: data.get('email'),


      } 
      let updatedTeams = [];
      teamList.map((data) => {
        currentTeams.map((currentTeam) => {
          if(data.name ==  currentTeam){
            updatedTeams.push(data.id);
          }
        })
       
      });

      postObject["teams"] = updatedTeams;

      axiosInstance
        .patch(`user/${userObj.id}/`, postObject)
        .then((res)=>{
            console.log(res);
            alert("Successfully changed account information");
            navigate('/dashboard');
      });

    }
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
                <InputLabel id="select-label">Teams</InputLabel>
                  <Select
                    label="Teams"
                    multiple
                    value={currentTeams}
                    onChange={handleTeamChange}
                    renderValue={(selected) => selected.join(', ')}
                  >
                   {/* <MenuItem key={1} value={1}>test</MenuItem> */}
                  {
                      // names = ['t1', 't2', 'TestTeam'];
                      teamList.map((team) => {
                 
                        return(
                          <MenuItem key={team.name} value={team.name}>
                          <Checkbox checked={currentTeams.indexOf(team.name) > -1} />
                          <ListItemText primary={team.name} />
                        </MenuItem>
                        )
                      })
                  }
                  </Select>
              </FormControl>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 , bgcolor: 'purple'}}
              >
                Submit Modifications
              </Button>

              {/* <Button
                type="changepassword"
                xs
                variant="contained"
                sx={{ mt: 3, mb: 2, ml: 15, alignContent: 'center', alignItems: 'center', bgcolor: 'orange'}}
                onClick={handleClickOpen}
              >
                Change Password
              </Button> */}
              <Grid container justifyContent="center" alignItems="center">
                <Grid item xs  >
                  <Typography paragraph >
                    <Link component="button" onClick={handleClickOpen} variant="body2" underline="none" 
                          sx={{ mt: 3, mb: 2, ml: 17.5, alignContent: 'center', alignItems: 'center', color: 'turqoise'}}>
                      Change password
                    </Link>
                  </Typography>
                </Grid>
                
              </Grid>
            </Box>
          </Box>
        </Container>


        <Dialog open={open} onClose={handleClose} >
        <DialogTitle>Change Password</DialogTitle>
        <DialogContent sx={{display: 'flex', flexDirection: 'column'}}>
          <DialogContentText>
            
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="old_password"
            label="Old Password"
            type="password"
            xs
            variant="standard"
            onChange={handleOldPasswordChange}
          />
          <TextField
            autoFocus
            margin="dense"
            id="new_password"
            label="New Password"
            type="password"
            xs
            variant="standard"
            onChange={handleNewPasswordChange}
            sx={{mt: 5}}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handlePasswordSubmit}>Change</Button>
        </DialogActions>
      </Dialog>

    </React.Fragment>
  );
}