import React, { useState, useEffect, Fragment } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';

function UsersTable() {

  const [usersList, setUsersList] = useState([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const [teamsList, setTeamsList] = useState([]);

  //modal state
  const [displayEditModal, setDisplayEditModal] = useState(false);
  let role_dict = {400: 'WORKER', 0: 'ORGANISATION_ADMIN', 100: 'ADMIN', 200: 'TEAM_LEADER', 300: 'OFFICE'};
  //Stores temporary form changes
  const [temporaryUser, setTemporaryUser] = useState({
    id: -1,
    first_name: "",
    last_name: "",
    email: "",
    role: ""
  });

  const clearState = () => {
    const formValues = {
      id: -1,
      first_name: '',
      last_name: '',
      email: '',
      role: '',
    };
    setTemporaryUser({ ...formValues });

    console.log("reset form data")
  };

  useEffect(() => {
    axiosInstance
      .get(`user/me/`, {
      })
      .then((res) => {
        console.log(res.data);
        if (res.data.role.level < 200) {
          setIsAdmin(true)
        }
      })
      .catch((err) => {
        alert("ERROR: user/me failed");
      });

    axiosInstance
      .get(`user/`, {
      })
      .then((res) => {
        res.data.map((data) => {
          setUsersList(usersList => [...usersList, data])
          console.log(res.data)
        })
      })
      .catch((err) => {
        alert("ERROR: Getting users failed");
      });

    //get the teams and store them
    axiosInstance
      .get(`teams/`, {
      })
      .then((res) => {
        res.data.map((data) => {
          setTeamsList(teamsList => [...teamsList, data])
          console.log(res.data)
        })
      })
      .catch((err) => {
        alert("ERROR: Getting teams failed");
      });
  }, []);

  const handleFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...temporaryUser };
    newFormData[fieldName] = fieldValue;

    setTemporaryUser({ ...newFormData });
  };

  const handleEditSubmit = () => {
    var postObject = {
      first_name: temporaryUser.first_name,
      last_name: temporaryUser.last_name,
      email: temporaryUser.email,
      // role: temporaryUser.role.level,
      // teams: temporaryUser.teams,
    }

    //Send PUT request to update user
    axiosInstance.put(`user/${temporaryUser.id}/`, postObject)

    //reset values
    clearState();

    //reload page
    window.location.reload();
  };

  const handleEditClick = (event, row) => {
    event.preventDefault();

    const formValues = {
      id: row.id,
      first_name: row.first_name,
      last_name: row.last_name,
      email: row.email,
      role: row.role.level,
    };
    setTemporaryUser({ ...formValues });

    //cause the modal to open.
    setDisplayEditModal(!displayEditModal);
  };

  const handleUserDelete = () => {
    axiosInstance.delete(`user/${temporaryUser.id}/`)
    clearState();
    window.location.reload();
  }

  return (
    <React.Fragment>
      <div className="main-content">
        <Typography variant="h4" sx={{
          fontFamily: 'Lato',
          fontWeight: 'bold',
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
                  <TableCell className="tableCell">{role_dict[row.role.level]}</TableCell>
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
        }}> Edit User</Typography>

        <form>
          <label>First Name:</label>
          <input
            type="text"
            name="first_name"
            required="required"
            placeholder="Enter a first name..."
            value={temporaryUser.first_name}
            onChange={handleFormChange}
            style={{ width: "200px" }}
          />
          <br></br>
          <label>Last Name:</label>
          <input
            type="text"
            name="last_name"
            required="required"
            placeholder="Enter a last name..."
            value={temporaryUser.last_name}
            onChange={handleFormChange}
            style={{ width: "200px" }}
          />
          <br></br>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            required="required"
            placeholder="Enter an email..."
            value={temporaryUser.email}
            onChange={handleFormChange}
            style={{ width: "200px" }}
          />
          <br></br>
          <label>Role:</label>
          <input
            type="text"
            name="role"
            required="required"
            placeholder="Enter a role..."
            value={temporaryUser.role.level}
            onChange={handleFormChange}
            style={{ width: "200px" }}
          />
          <br></br>
          <Button type="submit" variant="outlined" size="large" style={{
            color: "#028357",
            borderColor: "#028357",
          }}
            onClick={() => { setDisplayEditModal(!displayEditModal); handleEditSubmit() }}
          >Edit User</Button>
          <br></br>
          <Button type="submit" variant="outlined" size="large" style={{
            color: "#FF0000",
            borderColor: "#FF0000",
            margin: "20px",
          }}
            onClick={() => { handleUserDelete() }}
          >Delete User</Button>
        </form>
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