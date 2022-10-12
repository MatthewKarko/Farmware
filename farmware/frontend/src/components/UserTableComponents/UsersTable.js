import React, { useState, useEffect, Fragment } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/UsersTable.css';
import axiosInstance from '../../axios';

function UsersTable() {

  const [usersList, setUsersList] = useState([]);

  useEffect(() => {
    axiosInstance
      .get(`user/me/`, {
      })
      .then((res) => {
        console.log(res.data);
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
  }, []);


  const [displayEditModal, setDisplayEditModal] = useState(false);

  //Stores temporary changes
  const [temporaryUser, setTemporaryUser] = useState({
    first_name: "",
    last_name: "",
    email: "",
    role: ""
  });

  const clearState = () => {
    const formValues = {
      first_name: '',
      last_name: '',
      email: '',
      role: '',
    };
    setTemporaryUser({ ...formValues });

    console.log("reset form data")
  };

  const [editContactId, setEditContactId] = useState(null);

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
    console.log("Edit user submitted");

    const newUser = {
      first_name: temporaryUser.first_name,
      last_name: temporaryUser.last_name,
      email: temporaryUser.email,
      role: temporaryUser.role,
    };

    //TO DO: Send the UPDATE request from here based on newUser.
    console.log(newUser);

    //reset values
    clearState();
  };

  const handleEditClick = (event, row) => {
    event.preventDefault();
    setEditContactId(row.id);

    const formValues = {
      first_name: row.first_name,
      last_name: row.last_name,
      email: row.email,
      role: row.role,
    };
    // console.log("prior = " + temporaryUser.firstName);
    setTemporaryUser({ ...formValues });
    // console.log("after = " + temporaryUser.lastName);

    //Log the data that wants to be edited
    console.log("Edit button pressed for values:");
    console.log(formValues);

    //cause the modal to open.
    setDisplayEditModal(!displayEditModal);
  };

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
                <TableCell className="tableCell">Teams</TableCell>
                <TableCell className="tableCell">Edit</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {usersList.map((row) => (
                <TableRow key={row.id}>
                  <TableCell className="tableCell">{row.id}</TableCell>
                  <TableCell className="tableCell">{row.first_name}</TableCell>
                  <TableCell className="tableCell">{row.last_name}</TableCell>
                  <TableCell className="tableCell">{row.email}</TableCell>
                  <TableCell className="tableCell">{row.role}</TableCell>
                  <TableCell className="tableCell">{row.teams}</TableCell>
                  <TableCell className="tableCell">
                    <Button variant="outlined" size="medium"
                      style={{
                        color: "#028357",
                        borderColor: "#028357",
                      }}
                      onClick={(event) => handleEditClick(event, row)}
                    >Edit</Button>
                  </TableCell>
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

        <form onSubmit={handleEditSubmit}>
          <label>First Name:</label>
          <input
            type="text"
            name="firstName"
            required="required"
            placeholder="Enter a first name..."
            value={temporaryUser.first_name}
            onChange={handleFormChange}
            style={{width: "200px"}}
          />
          <br></br>
          <label>Last Name:</label>
          <input
            type="text"
            name="lastName"
            required="required"
            placeholder="Enter a last name..."
            value={temporaryUser.last_name}
            onChange={handleFormChange}
            style={{width: "200px"}}
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
            style={{width: "200px"}}
          />
          <br></br>
          <label>Role:</label>
          <input
            type="text"
            name="role"
            required="required"
            placeholder="Enter a role..."
            value={temporaryUser.role}
            onChange={handleFormChange}
            style={{width: "200px"}}
          />
          <br></br>
          <Button type="submit" variant="outlined" size="large" style={{
            color: "#028357",
            borderColor: "#028357",
          }}
            onClick={() => setDisplayEditModal(!displayEditModal)}
          >Submit</Button>
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