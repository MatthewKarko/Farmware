import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';
import { Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

function CustomersTable() {
    const navigate = useNavigate();

    const [customersList, setCustomersList] = useState([]);
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

    const [reloadFlag, setReloadFlag] = useState(false);
    const reloadCustomers = () => {
        setCustomersList([]);
        setReloadFlag(!reloadFlag); //prompts a reload of customers
    }
    
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
                // console.log(res.data);
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
                    setCustomersList(customersList => [...customersList, data])
                    // console.log(res.data)
                })
            })
            .catch((err) => {
                alert("ERROR: Getting customers failed");
            });
    }, [reloadFlag]);

    const handleFormChange = (event) => {
        event.preventDefault();

        const fieldName = event.target.getAttribute("name");
        const fieldValue = event.target.value;

        const newFormData = { ...temporaryCustomer };
        newFormData[fieldName] = fieldValue;

        setTemporaryCustomer({ ...newFormData });
    };

    const handleEditSubmit = (event) => {
        event.preventDefault();
        //VALIDATE temporaryCustomer.name (max: 50, non empty)
        if (temporaryCustomer.name.length > 50) {
            alert("ERROR: Invalid name input. Must be less than 50 characters long.")
            return;
        }
        if (temporaryCustomer.name.length < 1) {
            alert("ERROR: Invalid name input. Must not be empty.")
            return;
        }

        //VALIDATE temporaryCustomer.phone_number (max: 10, non empty)
        if (temporaryCustomer.phone_number.length > 10) {
            alert("ERROR: Invalid phone number input. Must be less than 10 digits.")
            return;
        }
        if (temporaryCustomer.phone_number.length < 1) {
            alert("ERROR: Invalid phone number input. Must not be empty.")
            return;
        }

        var putObject = {
            name: temporaryCustomer.name,
            phone_number: temporaryCustomer.phone_number,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.put(`customer/${temporaryCustomer.id}/`, putObject)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });

        //reset values
        clearState();

        //close modal
        setDisplayEditModal(!displayEditModal);
        
        reloadCustomers();
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

    const handleCustomerDelete = (event) => {
        event.preventDefault();
        axiosInstance.delete(`customer/${temporaryCustomer.id}/`)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });
        clearState();
        reloadCustomers();
    }

    const handleCreateSubmit = (event) => {
        event.preventDefault();
        //VALIDATE temporaryCustomer.name (max: 50, non empty)
        if (temporaryCustomer.name.length > 50) {
            alert("ERROR: Invalid name input. Must be less than 50 characters long.")
            return;
        }
        if (temporaryCustomer.name.length < 1) {
            alert("ERROR: Invalid name input. Must not be empty.")
            return;
        }

        //VALIDATE temporaryCustomer.phone_number (max: 10, non empty)
        if (temporaryCustomer.phone_number.length > 10) {
            alert("ERROR: Invalid phone number input. Must be less than 10 digits.")
            return;
        }
        if (temporaryCustomer.phone_number.length < 1) {
            alert("ERROR: Invalid phone number input. Must not be empty.")
            return;
        }

        var postObject = {
            name: temporaryCustomer.name,
            phone_number: temporaryCustomer.phone_number,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.post(`customer/`, postObject)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });

        //reset values
        clearState();

        //close modal
        setDisplayCreateModal(!displayCreateModal);

        //reload page
        reloadCustomers();
    };

    return (
        <React.Fragment>
            <div className="main-content">

                <Box sx={{ width: '100%', height: '10%' }}>
                    <Grid container rowSpacing={0} columnSpacing={{ xs: 6, sm: 2, md: 4 }}
                        style={{ minHeight: '10vh' }}>

                        <Grid item xs={6}>
                            <Typography variant="h4" sx={{
                                fontFamily: 'Lato',
                                fontWeight: 'bold',
                            }}> Customers Table</Typography>
                        </Grid>

                        <Grid item xs={6} sx={{ textAlign: "right" }}>
                            {isAdmin &&
                                <Button type="submit" variant="outlined" size="large" style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    margin: "20px",
                                }}
                                    onClick={() => { setDisplayCreateModal(!displayCreateModal) }}
                                >Create Customer</Button>
                            }
                        </Grid>
                    </Grid>
                </Box>


                <TableContainer component={Paper} style={{ margin: "auto" }}>
                    <Table aria-label="simple table" style={{ margin: "auto" }}>
                        <colgroup>
                            <col style={{ width: '15%' }} />
                            <col style={{ width: '40%' }} />
                            <col style={{ width: '30%' }} />
                            <col style={{ width: '15%' }} />
                        </colgroup>
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
                    mt: 2,
                    textAlign: "center"
                }}> Edit Customer</Typography>

                <Box component="form" onSubmit={handleEditSubmit} noValidate sx={{ mt: 2, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <TextField
                        xs
                        required
                        name="name"
                        margin="dense"
                        label="Supplier Name"
                        type="name"
                        id="name"
                        size="small"
                        autoComplete="name"
                        value={temporaryCustomer.name}
                        onChange={handleFormChange}
                        sx={{ mt: 2 }}
                        variant="filled"
                    />
                    <TextField
                        xs
                        required
                        margin="dense"
                        id="phone_number"
                        label="Phone Number"
                        name="phone_number"
                        autoComplete="phone_number"
                        autoFocus
                        size="small"
                        value={temporaryCustomer.phone_number}
                        onChange={handleFormChange}
                        sx={{ mt: 2 }}
                        variant="filled"

                    />


                    <Box noValidate>
                        <Button
                            type="normal"
                            variant="contained"
                            sx={{ mt: 3, mb: 2, bgcolor: 'green' }}
                            onClick={(event) => { handleEditSubmit }}
                        >
                            Submit
                        </Button>
                        <Button
                            type="delete"
                            variant="contained"
                            sx={{ mt: 3, mb: 2, ml: 2, bgcolor: 'red' }}
                            onClick={handleCustomerDelete}
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
                    mt: 2,
                    textAlign: 'center'
                }}> Create Customer</Typography>

                <Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <TextField
                        xs
                        required
                        name="name"
                        margin="dense"
                        label="Customer Name"
                        type="name"
                        id="name"
                        size="small"
                        autoComplete="name"
                        value={temporaryCustomer.name}
                        onChange={handleFormChange}
                        sx={{ mt: 2 }}
                        variant="filled"
                    />

                    <TextField
                        xs
                        required
                        margin="dense"
                        id="phone_number"
                        label="Phone Number"
                        name="phone_number"
                        autoComplete="phone_number"
                        autoFocus
                        size="small"
                        value={temporaryCustomer.phone_number}
                        onChange={handleFormChange}
                        sx={{ mt: 2 }}
                        variant="filled"

                    />

                    <Button
                        type="normal"
                        variant="contained"
                        sx={{ mt: 3, mb: 2, bgcolor: 'green' }}
                        onClick={(event) => { handleCreateSubmit }}
                    >
                        Create
                    </Button>



                </Box>
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