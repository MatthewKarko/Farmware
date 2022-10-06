import React, { useState, useEffect, Fragment } from "react";
import '../../css/UsersTable.css';
import data from "./mock-data.json";
import ReadOnlyRow from "./ReadOnlyRow";
import EditableRow from "./EditableRow";

//The resource that helped make the table: https://github.com/chrisblakely01/react-creating-a-table/tree/main/src

function UsersTable() {

  //This small snippet of code is for the modal
  const [alert, setAlert] = useState("");
  const [displayModal, setDisplayModal] = useState(false);


  const [contacts, setContacts] = useState(data);

  const [addFormData, setAddFormData] = useState({
    firstName: "",
    lastName: "",
    address: "",
    phoneNumber: "",
    email: "",
    role: "",
  });

  const [editFormData, setEditFormData] = useState({
    firstName: "",
    lastName: "",
    address: "",
    phoneNumber: "",
    email: "",
    role: "",
  });

  const [editContactId, setEditContactId] = useState(null);

  const handleAddFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...addFormData };
    newFormData[fieldName] = fieldValue;

    setAddFormData(newFormData);
  };

  const handleEditFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...editFormData };
    newFormData[fieldName] = fieldValue;

    setEditFormData(newFormData);
  };

  const handleAddFormSubmit = (event) => {
    event.preventDefault();

    const newContact = {
      firstName: addFormData.firstName,
      lastName: addFormData.lastName,
      address: addFormData.address,
      phoneNumber: addFormData.phoneNumber,
      email: addFormData.email,
      role: addFormData.role,
    };

    const newContacts = [...contacts, newContact];
    setContacts(newContacts);
  };

  const handleEditFormSubmit = (event) => {
    event.preventDefault();

    const editedContact = {
      id: editContactId,
      firstName: editFormData.firstName,
      lastName: editFormData.lastName,
      address: editFormData.address,
      phoneNumber: editFormData.phoneNumber,
      email: editFormData.email,
      role: editFormData.role,
    };

    const newContacts = [...contacts];

    const index = contacts.findIndex((contact) => contact.id === editContactId);

    newContacts[index] = editedContact;

    setContacts(newContacts);
    setEditContactId(null);
  };

  const handleEditClick = (event, contact) => {
    event.preventDefault();
    setEditContactId(contact.id);

    const formValues = {
      firstName: contact.firstName,
      lastName: contact.lastName,
      address: contact.address,
      phoneNumber: contact.phoneNumber,
      email: contact.email,
      role: contact.role,
    };

    setEditFormData(formValues);
  };

  const handleCancelClick = () => {
    setEditContactId(null);
  };

  const handleDeleteClick = (contactId) => {
    const newContacts = [...contacts];

    const index = contacts.findIndex((contact) => contact.id === contactId);

    newContacts.splice(index, 1);

    setContacts(newContacts);
  };

  return (
    <>
      <div className='offset' >
        <br></br>
        <h2>Users table</h2>

        <form onSubmit={handleEditFormSubmit}>
          <table>
            <thead>
              <tr>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Address</th>
                <th>Phone Number</th>
                <th>Email</th>
                <th>Role</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {contacts.map((contact) => (
                <Fragment>
                  {editContactId === contact.id ? (
                    <EditableRow
                      editFormData={editFormData}
                      handleEditFormChange={handleEditFormChange}
                      handleCancelClick={handleCancelClick}
                    />
                  ) : (
                    <ReadOnlyRow
                      contact={contact}
                      handleEditClick={handleEditClick}
                      handleDeleteClick={handleDeleteClick}
                    />
                  )}
                </Fragment>
              ))}
            </tbody>
          </table>
        </form>





    {/* Below is the code for the modal for the 'add user' button */}
        <button
      className="TriggerButton CenterAlign"
      onClick={() => setDisplayModal(!displayModal)}
    >
      Add Users
    </button>

    <div className={`Modal ${displayModal ? "Show" : ""}`}>
      <h3>Add new user:</h3>
      <button
        className="Close"
        onClick={() => setDisplayModal(!displayModal)}
      >
        X
      </button>

      <form onSubmit={handleAddFormSubmit}>
        <input
          type="text"
          name="firstName"
          required="required"
          placeholder="Enter a first name..."
          onChange={handleAddFormChange}
        />
        <input
          type="text"
          name="lastName"
          required="required"
          placeholder="Enter a last name..."
          onChange={handleAddFormChange}
        />
        <input
          type="text"
          name="address"
          required="required"
          placeholder="Enter an address..."
          onChange={handleAddFormChange}
        />
        <input
          type="text"
          name="phoneNumber"
          required="required"
          placeholder="Enter a phone number..."
          onChange={handleAddFormChange}
        />
        <input
          type="email"
          name="email"
          required="required"
          placeholder="Enter an email..."
          onChange={handleAddFormChange}
        />
        <input
          type="text"
          name="role"
          required="required"
          placeholder="Enter a role..."
          onChange={handleAddFormChange}
        />
        <button type="submit" onClick={() => setDisplayModal(!displayModal)}>Add</button>
      </form>
    </div>

    {/* Below snippet makes it so that if you click out of the modal it exits. */}
    <div
      className={`Overlay ${displayModal ? "Show" : ""}`}
      onClick={() => {setDisplayModal(!displayModal)}}
    />  
      </div>
    </>
  )
}

export default UsersTable