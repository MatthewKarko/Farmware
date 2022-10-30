import React, { useState, useEffect, Fragment } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import useNotification from "../alert/UseNotification";

function UsersTable() {
  const [msg, sendNotification] = useNotification();

  const [usersList, setUsersList] = useState([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const [teamList, setTeamlist] = useState([]);
  const [currentTeams, setCurrentTeams] = useState([]);
  const [currentRole, setCurrentRole] = useState(-1);

  //modal state
  const [displayEditModal, setDisplayEditModal] = useState(false);
  let role_dict = { 400: 'Worker', 0: 'Organisation Admin', 100: 'Admin', 200: 'Team Leader', 300: 'Office' };
  //Stores temporary form changes
  const [temporaryUser, setTemporaryUser] = useState({
    id: -1,
    first_name: "",
    last_name: "",
    email: "",
    role: ""
  });

  const [reloadFlag, setReloadFlag] = useState(false);
  const reloadUsers = () => {
    setUsersList([]);
    setTeamlist([]);
    setCurrentTeams([]);
    setReloadFlag(!reloadFlag); //prompts a reload of customers
  }

  const clearState = () => {
    const formValues = {
      id: -1,
      first_name: '',
      last_name: '',
      email: '',
      role: '',
    };
    setTemporaryUser({ ...formValues });

    // console.log("reset form data")
  };

  useEffect(() => {
    axiosInstance
      .get(`user/me/`, {
      })
      .then((res) => {
        // console.log(res.data);
        if (res.data.role.level < 200) {
          setIsAdmin(true)
        }
      })


    axiosInstance
      .get(`user/`, {
      })
      .then((res) => {
        res.data.map((data) => {
          setUsersList(usersList => [...usersList, data])
          // console.log(res.data)
        })
      })


    //get the teams and store them
    axiosInstance
      .get(`team/`, {
      })
      .then((res) => {
        res.data.map((data) => {
          setTeamlist(teamList => [...teamList, data])
          // console.log(res.data)
        })
      })

  }, [reloadFlag]);

  const handleTeamChange = (event) => {
    const {
      target: { value },
    } = event;
    setCurrentTeams(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const handleRoleChange = (event) => {
    event.preventDefault();

    setCurrentRole(event.target.value);
    console.log(event.target.value);

  };

  const handleFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...temporaryUser };
    newFormData[fieldName] = fieldValue;

    setTemporaryUser({ ...newFormData });
  };

  const handleEditSubmit = (event) => {
    event.preventDefault();
    if (temporaryUser.first_name.length > 50) {
      alert("ERROR: Invalid first name input. Must be less than 50 characters long.")
      return;
    }
    if (temporaryUser.first_name.length < 1) {
      alert("ERROR: Invalid first name input. Must not be empty.")
      return;
    }

    if (temporaryUser.last_name.length > 50) {
      alert("ERROR: Invalid last name input. Must be less than 50 characters long.")
      return;
    }
    if (temporaryUser.last_name.length < 1) {
      alert("ERROR: Invalid last name input. Must not be empty.")
      return;
    }

    if (temporaryUser.email.length < 1) {
      alert("ERROR: Invalid email input. Must not be empty.")
      return;
    }

    var postObject = {
      first_name: temporaryUser.first_name,
      last_name: temporaryUser.last_name,
      email: temporaryUser.email,
    }

    let updatedTeams = [];
    teamList.map((data) => {
      currentTeams.map((currentTeam) => {
        if (data.name == currentTeam) {
          updatedTeams.push(data.id);
        }
      })

    });

    postObject["teams"] = updatedTeams;
    postObject["role"] = currentRole;
    // console.log(postObject)
    //Send PUT request to update user
    axiosInstance.put(`user/${temporaryUser.id}/`, postObject)
      .catch((err) => {
        alert("Error code: " + err.response.status + "\n" + err.response.data.error);
      });

    //reset values
    // clearState();

    reloadUsers();

    setDisplayEditModal(!displayEditModal);

    sendNotification({msg: 'Success: User Updated', variant: 'success'});
  };

  const handleEditClick = (event, row) => {
    event.preventDefault();

    const formValues = {
      id: row.id,
      first_name: row.first_name,
      last_name: row.last_name,
      email: row.email,
      role: row.role.name,
    };
    axiosInstance
      .get(`user/${row.id}/teams/`, {
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
    setTemporaryUser({ ...formValues });
    setCurrentRole(row.role.level);
    //cause the modal to open.
    setDisplayEditModal(!displayEditModal);
  };

  const handleUserDelete = (event) => {
    event.preventDefault();
    axiosInstance.delete(`user/${temporaryUser.id}/`)
      .catch((err) => {
        alert("Error code: " + err.response.status + "\n" + err.response.data.error);
      });
    clearState();
    setDisplayEditModal(!displayEditModal);
    reloadUsers();
    sendNotification({msg: 'Success: User Deleted', variant: 'success'});
  }


  return (
    <React.Fragment>
      <div className="main-content">
        <Typography variant="h4" sx={{
          fontFamily: 'Lato',
          fontWeight: 'bold',
          mb: 2
        }}> Users Table</Typography>
        <TableContainer component={Paper}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell className="tableCell">ID</TableCell>
                <TableCell className="tableCell">First Name</TableCell>
                <TableCell className="tableCell">Last Name</TableCell>
                <TableCell className="tableCell">Email</TableCell>
                <TableCell className="tableCell">Role</TableCell>
                {isAdmin && < TableCell className="tableCell">Edit</TableCell>}
              </TableRow>
            </TableHead>
            <TableBody>
              {usersList.map((row) => (
                <TableRow key={row.id}>
                  <TableCell className="tableCell">{row.id}</TableCell>
                  <TableCell className="tableCell">{row.first_name}</TableCell>
                  <TableCell className="tableCell">{row.last_name}</TableCell>
                  <TableCell className="tableCell">{row.email}</TableCell>
                  <TableCell className="tableCell">{row.role.name}</TableCell>
                  {isAdmin &&
                    <TableCell className="tableCell">
                      <Button variant="outlined" size="medium"
                        onClick={(event) => handleEditClick(event, row)}
                      >Edit</Button>
                    </TableCell>
                  }
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>

      {/* The modal is currently not in MUI components, might change it to MUI later */}
      <div className={`Modal ${displayEditModal ? "Show" : ""}`}>
        <button
          className="Close"
          onClick={() => { setDisplayEditModal(!displayEditModal); clearState(); }}
        >
          X
        </button>

        <Typography variant="h4" sx={{
          fontFamily: 'Lato',
          fontWeight: 'bold',
          margin: "20px",
          mt: 2,
          textAlign: 'center'
        }}> Edit User</Typography>


        <Box component="form" onSubmit={handleEditSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Box noValidate>
            <TextField
              required
              margin="normal"
              id="first_name"
              label="Firstname"
              name="first_name"
              autoComplete="first_name"
              autoFocus
              size="small"
              value={temporaryUser.first_name}
              onChange={handleFormChange}
              sx={{ width: "200px" }}
              variant="filled"

            />
            <TextField
              required
              margin="dense"
              name="last_name"
              label="Lastname"
              type="last_name"
              id="last_name"
              autoComplete="last_name"
              size="small"
              value={temporaryUser.last_name}
              onChange={handleFormChange}
              sx={{ width: "200px", mt: 2, ml: 2 }}
              variant="filled"
            />
          </Box>
          <TextField
            required
            margin="dense"
            name="email"
            label="Email Address"
            type="email"
            id="email"
            autoComplete="email"
            size="small"
            value={temporaryUser.email}
            onChange={handleFormChange}
            sx={{ width: "420px", mt: 1 }}
            variant="filled"
          />
          <Box noValidate>
            <FormControl sx={{ width: "200px", mt: 1 }} >
              <InputLabel id="demo-simple-select-label">Teams</InputLabel>
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

                    return (
                      <MenuItem key={team.name} value={team.name}>
                        <Checkbox checked={currentTeams.indexOf(team.name) > -1} />
                        <ListItemText primary={team.name} />
                      </MenuItem>
                    )
                  })
                }
              </Select>
            </FormControl>
            <FormControl sx={{ width: "200px", mt: 1, ml: 2 }} >
              <InputLabel id="select-label">Role</InputLabel>
              <Select
                label="Role"
                value={currentRole}
                onChange={handleRoleChange}
              >
                {

                  Object.entries(role_dict).map(([key, value]) => {
                    return (
                      <MenuItem key={key} value={key}>
                        {value}
                      </MenuItem>
                    )

                  })
                }
              </Select>
            </FormControl>
          </Box>
          <Box noValidate>
            <Button
              type="submit"
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Submit
            </Button>
            <Button
              type="delete"
              variant="contained"
              sx={{ mt: 3, mb: 2, ml: 2, bgcolor: 'red' }}
              onClick={handleUserDelete}
            >
              Delete
            </Button>

          </Box>

        </Box>
      </div>

      {/* Below snippet makes it so that if you click out of the modal it exits. */}
      <div
        className={`Overlay ${displayEditModal ? "Show" : ""}`}
        onClick={() => { setDisplayEditModal(!displayEditModal); clearState(); }}
      />
    </React.Fragment>
  )
}

export default UsersTable