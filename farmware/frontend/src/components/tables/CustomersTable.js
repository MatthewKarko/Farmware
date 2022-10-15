import React, { useState, useEffect, Fragment } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';

function CustomersTable() {

    const [customersList, setcustomersList] = useState([]);
    const [isAdmin, setIsAdmin] = useState(false);
    const [organisationCode, setOrganisationCode] = useState("");

    //   Modal states
    const [displayEditModal, setDisplayEditModal] = useState(false);
    const [displayCreateModal, setDisplayCreateModal] = useState(false);

    //Stores temporary changes
    const [temporaryCustomer, setTemporaryCustomer] = useState({
        id: -1,
        name: "",
        phone_number: "",
    });

    const clearState = () => {
        const formValues = {
            id: -1,
            name: "",
            phone_number: "",
        };
        setTemporaryCustomer({ ...formValues });
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
                // Set the organisation code as well
                setOrganisationCode(res.data.organisation)
            })
            .catch((err) => {
                alert("ERROR: user/me failed");
            });

        axiosInstance
            .get(`customer/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setcustomersList(customersList => [...customersList, data])
                    console.log(res.data)
                })
            })
            .catch((err) => {
                alert("ERROR: Getting customers failed");
            });
    }, []);


    const handleFormChange = (event) => {
        event.preventDefault();

        const fieldName = event.target.getAttribute("name");
        const fieldValue = event.target.value;

        const newFormData = { ...temporaryCustomer };
        newFormData[fieldName] = fieldValue;

        setTemporaryCustomer({ ...newFormData });
    };

    const handleEditSubmit = () => {

        var putObject = {
            name: temporaryCustomer.name,
            phone_number: temporaryCustomer.phone_number,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.put(`customer/${temporaryCustomer.id}/`, putObject)

        //reset values
        clearState();

        //close modal
        setDisplayEditModal(!displayEditModal);

        //reload page
        window.location.reload();
    };

    const handleEditClick = (event, row) => {
        event.preventDefault();

        const formValues = {
            id: row.id,
            name: row.name,
            phone_number: row.phone_number,
        };
        setTemporaryCustomer({ ...formValues });

        //cause the modal to open.
        setDisplayEditModal(!displayEditModal);
    };

    const handleCustomerDelete = () => {
        axiosInstance.delete(`customer/${temporaryCustomer.id}/`)
        clearState();
        window.location.reload();
    }

    const handleCreateSubmit = () => {
        var postObject = {
            name: temporaryCustomer.name,
            phone_number: temporaryCustomer.phone_number,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.post(`customer/`, postObject)

        //reset values
        clearState();

        //close modal
        setDisplayCreateModal(!displayCreateModal);

        //reload page
        window.location.reload();
    };

    return (
        <React.Fragment>
            <div className="main-content">
                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                }}> Customers Table</Typography>

                <Button type="submit" variant="outlined" size="large" style={{
                    color: "#028357",
                    borderColor: "#028357",
                    margin: "20px",
                }}
                    onClick={() => { setDisplayCreateModal(!displayCreateModal) }}
                >Create Customer</Button>

                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell className="tableCell">ID</TableCell>
                                <TableCell className="tableCell">Name</TableCell>
                                <TableCell className="tableCell">Phone Number</TableCell>
                                {isAdmin && < TableCell className="tableCell">Edit</TableCell>}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {customersList.map((row) => (
                                <TableRow key={row.id}>
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.name}</TableCell>
                                    <TableCell className="tableCell">{row.phone_number}</TableCell>
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

            {/* Modal for EDIT customer */}
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
                }}> Edit Customer</Typography>

                <form>
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        required="required"
                        placeholder="Enter a name..."
                        value={temporaryCustomer.name}
                        onChange={handleFormChange}
                        style={{ width: "200px" }}
                    />
                    <br></br>
                    <label>Phone Number:</label>
                    <input
                        type="text"
                        name="phone_number"
                        required="required"
                        placeholder="Enter a phone number..."
                        value={temporaryCustomer.phone_number}
                        onChange={handleFormChange}
                        style={{ width: "200px" }}
                    />
                    <br></br>
                    <Button type="submit" variant="outlined" size="large" style={{
                        color: "#028357",
                        borderColor: "#028357",
                        margin: "8px",
                    }}
                        onClick={() => { handleEditSubmit() }}
                    >Submit</Button>
                    <br></br>
                    <Button type="submit" variant="outlined" size="large" style={{
                        color: "#FF0000",
                        borderColor: "#FF0000",
                        margin: "8px",
                    }}
                        onClick={() => { handleCustomerDelete() }}
                    >Delete Customer</Button>
                </form>
            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayEditModal ? "Show" : ""}`}
                onClick={() => { setDisplayEditModal(!displayEditModal); clearState(); }}
            />

        
         {/* Modal for CREATE customer */}
         <div className={`Modal ${displayCreateModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayCreateModal(!displayCreateModal); clearState(); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    margin: "20px",
                }}> Create Customer</Typography>

                <form>
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        required="required"
                        placeholder="Enter a name..."
                        value={temporaryCustomer.name}
                        onChange={handleFormChange}
                        style={{ width: "200px" }}
                    />
                    <br></br>
                    <label>Phone Number:</label>
                    <input
                        type="text"
                        name="phone_number"
                        required="required"
                        placeholder="Enter a phone number..."
                        value={temporaryCustomer.phone_number}
                        onChange={handleFormChange}
                        style={{ width: "200px" }}
                    />
                    <br></br>
                    <Button type="submit" variant="outlined" size="large" style={{
                        color: "#028357",
                        borderColor: "#028357",
                        margin: "8px",
                    }}
                        onClick={() => { handleCreateSubmit() }}
                    >Create</Button>
                    <br></br>
                </form>
            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayCreateModal ? "Show" : ""}`}
                onClick={() => { setDisplayCreateModal(!displayCreateModal); clearState(); }}
            />

        </React.Fragment>
    )
}

export default CustomersTable