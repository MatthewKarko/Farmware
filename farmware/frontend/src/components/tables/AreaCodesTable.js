import React, { useState, useEffect, Fragment } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

function AreaCodesTable() {

    const [areaCodesList, setAreaCodesList] = useState([]);
    const [organisationCode, setOrganisationCode] = useState("");

    //   Modal states
    const [displayEditModal, setDisplayEditModal] = useState(false);
    const [displayCreateModal, setDisplayCreateModal] = useState(false);

    //Stores temporary changes
    const [temporaryAreaCode, setTemporaryAreaCode] = useState({
        id: -1,
        area_code: "",
        description: "",
    });

    const clearState = () => {
        const formValues = {
            id: -1,
        area_code: "",
        description: "",
        };
        setTemporaryAreaCode({ ...formValues });
    };

    useEffect(() => {
        axiosInstance
            .get(`user/me/`, {
            })
            .then((res) => {
                console.log(res.data);
                // Set the organisation code as well
                setOrganisationCode(res.data.organisation)
            })
            .catch((err) => {
                alert("ERROR: user/me failed");
            });

        axiosInstance
            .get(`area_code/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setAreaCodesList(areaCodesList => [...areaCodesList, data])
                    console.log(res.data)
                })
            })
            .catch((err) => {
                alert("ERROR: Getting area_code failed");
            });
    }, []);


    const handleFormChange = (event) => {
        event.preventDefault();

        const fieldName = event.target.getAttribute("name");
        const fieldValue = event.target.value;

        const newFormData = { ...temporaryAreaCode };
        newFormData[fieldName] = fieldValue;

        setTemporaryAreaCode({ ...newFormData });
    };

    const handleEditSubmit = () => {

        var putObject = {
            area_code: temporaryAreaCode.area_code,
            description: temporaryAreaCode.description,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.put(`area_code/${temporaryAreaCode.id}/`, putObject)

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
            area_code: row.area_code,
            description: row.description,
        };
        setTemporaryAreaCode({ ...formValues });

        //cause the modal to open.
        setDisplayEditModal(!displayEditModal);
    };

    const handleAreaCodeDelete = (event) => {
        event.preventDefault();
        axiosInstance.delete(`area_code/${temporaryAreaCode.id}/`)
        clearState();
        window.location.reload();
    }

    const handleCreateSubmit = () => {
        var postObject = {
            area_code: temporaryAreaCode.area_code,
            description: temporaryAreaCode.description,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.post(`area_code/`, postObject)

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
                }}> Area Codes Table</Typography>

                <Button type="submit" variant="outlined" size="large" style={{
                    color: "#028357",
                    borderColor: "#028357",
                    margin: "20px",
                }}
                    onClick={() => { setDisplayCreateModal(!displayCreateModal) }}
                >Create Area Code</Button>
                

                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell className="tableCell">ID</TableCell>
                                <TableCell className="tableCell">Area Code</TableCell>
                                <TableCell className="tableCell">Description</TableCell>
                                < TableCell className="tableCell">Edit</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {areaCodesList.map((row) => (
                                <TableRow key={row.id}>
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.area_code}</TableCell>
                                    <TableCell className="tableCell">{row.description}</TableCell>
                                        <TableCell className="tableCell">
                                            <Button variant="outlined" size="medium"
                                                onClick={(event) => handleEditClick(event, row)}
                                            >Edit</Button>
                                        </TableCell>
                                    
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>

            {/* Modal for EDIT area code */}
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
                }}> Edit Area Code</Typography>

                <Box component="form" onSubmit={handleEditSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
 
                    <TextField
                    xs
                        required
                        margin="dense"
                        id="area_code"
                        label="Area Code"
                        name="area_code"
                        autoComplete="area_code"
                        autoFocus
                        size="small"
                        value={temporaryAreaCode.area_code}
                        onChange={handleFormChange}
                        // sx={{width: "250px"}}
                        variant="filled"
                        
                    />
                    <TextField
                        xs
                        required
                        name="description"
                        margin="dense"
                        label="Description"
                        type="description"
                        id="description"
                        size="small"
                        autoComplete="name"
                        value={temporaryAreaCode.description}
                        onChange={handleFormChange}
                        sx={{ mt: 2}}
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
                            sx={{ mt: 3, mb: 2, ml: 2,  bgcolor: 'red' }}
                            onClick={handleAreaCodeDelete}
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


            {/* Modal for CREATE area code */}
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
                }}> Create Area Code</Typography>

<Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <TextField
                        xs
                        required
                        name="area_code"
                        margin="dense"
                        label="Area code"
                        type="area_code"
                        id="area_code"
                        size="small"
                        autoComplete="area_code"
                        value={temporaryAreaCode.area_code}
                        onChange={handleFormChange}
                        sx={{ mt: 2}}
                        variant="filled"
                    />

                    <TextField
                    xs
                        required
                        margin="dense"
                        id="description"
                        label="Description"
                        name="description"
                        autoComplete="description"
                        autoFocus
                        size="small"
                        value={temporaryAreaCode.description}
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

export default AreaCodesTable