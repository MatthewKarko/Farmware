import React, { useState, useEffect, Fragment } from "react";
import data from "./mock-data.json";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/UsersTable.css';

function UsersTable() {

  const [displayEditModal, setDisplayEditModal] = useState(false);
  const [displayNewModal, setDisplayNewModal] = useState(false);

  //Stores temporary changes
  const [temporaryUser, setTemporaryUser] = useState({
    firstName: "",
    lastName: "",
    address: "",
    phoneNumber: "",
    email: "",
    role: ""
  });

  const clearState = () => {
    const formValues = {
      firstName: '',
      lastName: '',
      address: '',
      phoneNumber: '',
      email: '',
      role: '',
    };
    setTemporaryUser({ ...formValues });

    console.log("reset form data")
  };

  const [editContactId, setEditContactId] = useState(null);

  const handleAddFormChange = (event) => {
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
      firstName: temporaryUser.firstName,
      lastName: temporaryUser.lastName,
      address: temporaryUser.address,
      phoneNumber: temporaryUser.phoneNumber,
      email: temporaryUser.email,
      role: temporaryUser.role,
    };

    //TO DO: Send the UPDATE request from here based on newUser.
    console.log(newUser);

    //reset values
    clearState();
  };

  const handleNewUserSubmit = (event) => {
    event.preventDefault();

    const newUser = {
      firstName: temporaryUser.firstName,
      lastName: temporaryUser.lastName,
      address: temporaryUser.address,
      phoneNumber: temporaryUser.phoneNumber,
      email: temporaryUser.email,
      role: temporaryUser.role,
    };

    //TO DO: Send the POST request from here based on newUser.
    console.log("New user submitted");
    console.log(newUser);

    //reset edit form
    clearState();
  };

  const handleEditClick = (event, row) => {
    event.preventDefault();
    setEditContactId(row.id);

    const formValues = {
      firstName: row.firstName,
      lastName: row.lastName,
      address: row.address,
      phoneNumber: row.phoneNumber,
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
    <>
      <React.Fragment>
        <Typography variant="h4" sx={{
          fontFamily: 'Lato',
          fontWeight: 'bold',
        }}> Users Table</Typography>
        <TableContainer component={Paper}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell className="tableCell">ID</TableCell>
                <TableCell className="tableCell">First name</TableCell>
                <TableCell className="tableCell">Last name</TableCell>
                <TableCell className="tableCell">Address</TableCell>
                <TableCell className="tableCell">Phone Number</TableCell>
                <TableCell className="tableCell">Email</TableCell>
                <TableCell className="tableCell">Role</TableCell>
                <TableCell className="tableCell">Edit</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row) => (
                <TableRow key={row.id}>
                  <TableCell className="tableCell">{row.id}</TableCell>
                  <TableCell className="tableCell">{row.firstName}</TableCell>
                  <TableCell className="tableCell">{row.lastName}</TableCell>
                  <TableCell className="tableCell">{row.address}</TableCell>
                  <TableCell className="tableCell">{row.phoneNumber}</TableCell>
                  <TableCell className="tableCell">{row.email}</TableCell>
                  <TableCell className="tableCell">{row.role}</TableCell>
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
              value={temporaryUser.firstName}
              onChange={handleAddFormChange}
            />
            <br></br>
            <label>Last Name:</label>
            <input
              type="text"
              name="lastName"
              required="required"
              placeholder="Enter a last name..."
              value={temporaryUser.lastName}
              onChange={handleAddFormChange}
            />
            <br></br>
            <label>Address:</label>
            <input
              type="text"
              name="address"
              required="required"
              placeholder="Enter an address..."
              value={temporaryUser.address}
              onChange={handleAddFormChange}
            /><br></br>
            <label>Phone Number:</label>
            <input
              type="text"
              name="phoneNumber"
              required="required"
              placeholder="Enter a phone number..."
              value={temporaryUser.phoneNumber}
              onChange={handleAddFormChange}
            />
            <br></br>
            <label>Email:</label>
            <input
              type="email"
              name="email"
              required="required"
              placeholder="Enter an email..."
              value={temporaryUser.email}
              onChange={handleAddFormChange}
            />
            <br></br>
            <label>Role:</label>
            <input
              type="text"
              name="role"
              required="required"
              placeholder="Enter a role..."
              value={temporaryUser.role}
              onChange={handleAddFormChange}
            />
            <br></br>
            <Button type="submit" variant="outlined" size="large" style={{
              color: "#028357",
              borderColor: "#028357",
            }}
              onClick={() => setDisplayEditModal(!displayEditModal)}
            >Add</Button>
          </form>
        </div>

        {/* Below snippet makes it so that if you click out of the modal it exits. */}
        <div
          className={`Overlay ${displayEditModal ? "Show" : ""}`}
          onClick={() => { setDisplayEditModal(!displayEditModal); clearState(); }}
        />
      </React.Fragment>
    </>
  )
}

export default UsersTable