import React, { useState, useEffect, Fragment } from "react";
import data from "./mock-data.json";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Button from '@mui/material/Button';
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
    setTemporaryUser({...formValues});
    
    console.log("reset form data")
  };

  const [editContactId, setEditContactId] = useState(null);

  const handleAddFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...temporaryUser };
    newFormData[fieldName] = fieldValue;

    setTemporaryUser({...newFormData});
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
    setTemporaryUser({...formValues});
    // console.log("after = " + temporaryUser.lastName);

    //Log the data that wants to be edited
    console.log("Edit button pressed for values:");
    console.log(formValues);

    //cause the modal to open.
    setDisplayEditModal(!displayEditModal);
  };

  return (
    <>
      <div className="body">
        <br></br>
        <h2>Users table</h2>
        <TableContainer component={Paper} className="table">
      <Table sx={{ minWidth: 650}} aria-label="simple table">
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
                  <Button variant="outlined" size="medium" onClick={(event) => handleEditClick(event, row)}
            >Edit</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>

    {/* Create add new user button */}
    <br></br>
    <Button variant="outlined" size="large" onClick={() => {setDisplayNewModal(!displayNewModal);}}
        >Add new user</Button>


    <div className={`Modal ${displayEditModal ? "Show" : ""}`}>
      <button
        className="Close"
        onClick={() => {setDisplayEditModal(!displayEditModal); clearState();} }
      >
        X
      </button>
      
      <h1>Edit User</h1>

      <form onSubmit={handleEditSubmit}>
      <label>First Name:</label>
        <input
          type="text"
          name="firstName"
          required="required"
          placeholder="Enter a first name..."
          value={temporaryUser.firstName}
          onChange={handleAddFormChange}
        /><br></br>
        <label>Last Name:</label>
        <input
          type="text"
          name="lastName"
          required="required"
          placeholder="Enter a last name..."
          value={temporaryUser.lastName}
          onChange={handleAddFormChange}
        /><br></br>
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
        /><br></br>
        <label>Email:</label>
        <input
          type="email"
          name="email"
          required="required"
          placeholder="Enter an email..."
          value={temporaryUser.email}
          onChange={handleAddFormChange}
        /><br></br>
        <label>Role:</label>
        <input
          type="text"
          name="role"
          required="required"
          placeholder="Enter a role..."
          value={temporaryUser.role}
          onChange={handleAddFormChange}
        /><br></br>
        <Button type="submit" variant="outlined" size="large" onClick={() => setDisplayEditModal(!displayEditModal)}
            >Add</Button>
      </form>
      </div>

    {/* Below snippet makes it so that if you click out of the modal it exits. */}
    <div
      className={`Overlay ${displayEditModal ? "Show" : ""}`}
      onClick={() => {setDisplayEditModal(!displayEditModal); clearState();}}
    /> 



<div className={`Modal ${displayNewModal ? "Show" : ""}`}>
      <button
        className="Close"
        onClick={() => {setDisplayNewModal(!displayNewModal); clearState();}}
      >
        X
      </button>
      
      <h1>Create New User</h1>

      <form onSubmit={handleNewUserSubmit} className='formUsers'>
      <label>First Name:</label>
        <input
          type="text"
          name="firstName"
          required="required"
          // placeholder="Enter a first name..."
          value={temporaryUser.firstName}
          onChange={handleAddFormChange}
        /><br></br>
        <label>Last Name:</label>
        <input
          type="text"
          name="lastName"
          required="required"
          // placeholder="Enter a last name..."
          value={temporaryUser.lastName}
          onChange={handleAddFormChange}
        /><br></br>
        <label>Address:</label>
        <input
          type="text"
          name="address"
          required="required"
          // placeholder="Enter an address..."
          value={temporaryUser.address}
          onChange={handleAddFormChange}
        /><br></br>
        <label>Phone Number:</label>
        <input
          type="text"
          name="phoneNumber"
          required="required"
          // placeholder="Enter a phone number..."
          value={temporaryUser.phoneNumber}
          onChange={handleAddFormChange}
        /><br></br>
        <label>Email:</label>
        <input
          type="email"
          name="email"
          required="required"
          // placeholder="Enter an email..."
          value={temporaryUser.email}
          onChange={handleAddFormChange}
        /><br></br>
        <label>Role:</label>
        <input
          type="text"
          name="role"
          required="required"
          // placeholder="Enter a role..."
          value={temporaryUser.role}
          onChange={handleAddFormChange}
        /><br></br>
        <Button type="submit" variant="outlined" size="large" onClick={() => setDisplayEditModal(!displayNewModal)}
            >Add</Button>
      </form>
      </div>

    {/* Below snippet makes it so that if you click out of the modal it exits. */}
    <div
      className={`Overlay ${displayNewModal ? "Show" : ""}`}
      onClick={() => {setDisplayNewModal(!displayNewModal); clearState();}}
    />
      </div>
    </>
  )
}

export default UsersTable