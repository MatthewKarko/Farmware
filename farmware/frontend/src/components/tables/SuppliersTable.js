import React, { useState, useEffect, Fragment } from "react";
import { Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

function SuppliersPage() {

    const [suppliersList, setSuppliersList] = useState([]);
    const [isAdmin, setIsAdmin] = useState(false);
    const [organisationCode, setOrganisationCode] = useState("");

    //   Modal states
    const [displayEditModal, setDisplayEditModal] = useState(false);
    const [displayCreateModal, setDisplayCreateModal] = useState(false);

    //Stores temporary changes
    const [temporarySupplier, setTemporarySupplier] = useState({
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
        setTemporarySupplier({ ...formValues });
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
            .get(`supplier/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setSuppliersList(suppliersList => [...suppliersList, data])
                    console.log(res.data)
                })
            })
            .catch((err) => {
                alert("ERROR: Getting suppliers failed");
            });
    }, []);


    const handleFormChange = (event) => {
        event.preventDefault();

        const fieldName = event.target.getAttribute("name");
        const fieldValue = event.target.value;

        const newFormData = { ...temporarySupplier };
        newFormData[fieldName] = fieldValue;

        setTemporarySupplier({ ...newFormData });
    };

    const handleEditSubmit = () => {

        var putObject = {
            name: temporarySupplier.name,
            phone_number: temporarySupplier.phone_number,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.put(`supplier/${temporarySupplier.id}/`, putObject)

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
        setTemporarySupplier({ ...formValues });

        //cause the modal to open.
        setDisplayEditModal(!displayEditModal);
    };

    const handleSupplierDelete = (event) => {
        event.preventDefault();
        axiosInstance.delete(`supplier/${temporarySupplier.id}/`)
        clearState();
        window.location.reload();
    }

    const handleCreateSubmit = () => {
        var postObject = {
            name: temporarySupplier.name,
            phone_number: temporarySupplier.phone_number,
            organisation: organisationCode,
        }


        axiosInstance.post(`supplier/`, postObject);
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
                            }}> Suppliers Table</Typography>
                        </Grid>

                        <Grid item xs={6} sx={{ textAlign: "right" }}>
                            {isAdmin &&
                                <Button type="submit" variant="outlined" size="large" style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    margin: "20px",
                                }}
                                    onClick={() => { setDisplayCreateModal(!displayCreateModal) }}
                                >Create Supplier</Button>
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
                            {suppliersList.map((row) => (
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

            {/* Modal for EDIT supplier */}
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
                    textAlign: 'center'
                }}> Edit Supplier</Typography>

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
                        value={temporarySupplier.name}
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
                        value={temporarySupplier.phone_number}
                        onChange={handleFormChange}
                        sx={{ mt: 2 }}
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
                            onClick={handleSupplierDelete}
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


            {/* Modal for CREATE supplier */}
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
                }}> Create Supplier</Typography>
                <Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <TextField
                        xs
                        required
                        name="name"
                        margin="dense"
                        label="Supplier name"
                        type="name"
                        id="name"
                        size="small"
                        autoComplete="name"
                        value={temporarySupplier.name}
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
                        value={temporarySupplier.phone_number}
                        onChange={handleFormChange}
                        sx={{ mt: 2 }}
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

                {/* <form>
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        required="required"
                        placeholder="Enter a name..."
                        value={temporarySupplier.name}
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
                        value={temporarySupplier.phone_number}
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
                </form> */}
            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayCreateModal ? "Show" : ""}`}
                onClick={() => { setDisplayCreateModal(!displayCreateModal); clearState(); }}
            />

        </React.Fragment>
    )
}

export default SuppliersPage