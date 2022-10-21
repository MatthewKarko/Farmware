import React, { useState, useEffect, Fragment } from "react";
import { Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
function CustomersTable() {

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
                    setCustomersList(customersList => [...customersList, data])
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

    const handleCustomerDelete = (event) => {
        event.preventDefault();
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

                <Box component="form" onSubmit={handleEditSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
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
                        // sx={{width: "250px"}}
                        variant="filled"

                    />


                    <Box noValidate>
                        <Button
                            type="submit"
                            variant="contained"
                            sx={{ mt: 3, mb: 2, bgcolor: 'green' }}
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

                {/* <form>
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
                </form> */}
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
                        // sx={{width: "250px"}}
                        variant="filled"

                    />



                    <Button
                        type="create"
                        variant="contained"
                        sx={{ mt: 3, mb: 2, bgcolor: 'green' }}
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