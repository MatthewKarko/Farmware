import React, { useState, useEffect, Fragment } from "react";
import { Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

function TeamsPage() {

    const [teamsList, setTeamsList] = useState([]);
    const [organisationCode, setOrganisationCode] = useState("");

    //   Modal states
    const [displayEditModal, setDisplayEditModal] = useState(false);
    const [displayCreateModal, setDisplayCreateModal] = useState(false);

    //Stores temporary changes
    const [temporaryTeam, setTemporaryTeam] = useState({
        id: -1,
        category: "",
        name: "",
    });

    const clearState = () => {
        const formValues = {
            id: -1,
            category: "",
            name: "",
        };
        setTemporaryTeam({ ...formValues });
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
            .get(`team/`, {
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

        const newFormData = { ...temporaryTeam };
        newFormData[fieldName] = fieldValue;

        setTemporaryTeam({ ...newFormData });
    };

    const handleEditSubmit = (event) => {
        event.preventDefault();
        var putObject = {
            category: temporaryTeam.category,
            name: temporaryTeam.name,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.put(`teams/${temporaryTeam.id}/`, putObject)

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
            category: row.category,
            name: row.name,
        };
        setTemporaryTeam({ ...formValues });

        //cause the modal to open.
        setDisplayEditModal(!displayEditModal);
    };

    const handleTeamDelete = (event) => {
        event.preventDefault();
        axiosInstance.delete(`teams/${temporaryTeam.id}/`)
        clearState();
        window.location.reload();
    }

    const handleCreateSubmit = () => {
        var postObject = {
            category: temporaryTeam.category,
            name: temporaryTeam.name,
            organisation: organisationCode,
        }

        //Send PUT request to update user
        axiosInstance.post(`teams/`, postObject)

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
                            }}> Teams Table</Typography>
                        </Grid>

                        <Grid item xs={6} sx={{ textAlign: "right" }}>
                            <Button type="submit" variant="outlined" size="large" style={{
                                color: "#028357",
                                borderColor: "#028357",
                                margin: "20px",
                            }}
                                onClick={() => { setDisplayCreateModal(!displayCreateModal) }}
                            >Create Team</Button>
                        </Grid>
                    </Grid>
                </Box>


                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell className="tableCell">ID</TableCell>
                                <TableCell className="tableCell">Category</TableCell>
                                <TableCell className="tableCell">Team Name</TableCell>
                                < TableCell className="tableCell">Edit</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {teamsList.map((row) => (
                                <TableRow key={row.id}>
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.category}</TableCell>
                                    <TableCell className="tableCell">{row.name}</TableCell>
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

            {/* Modal for EDIT team */}
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
                }}> Edit Team</Typography>

                <Box component="form" onSubmit={handleEditSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <TextField
                        xs
                        required
                        margin="dense"
                        id="category"
                        label="Category"
                        name="category"
                        autoComplete="category"
                        autoFocus
                        size="small"
                        value={temporaryTeam.category}
                        onChange={handleFormChange}
                        // sx={{width: "250px"}}
                        variant="filled"

                    />
                    <TextField
                        xs
                        required
                        name="name"
                        margin="dense"
                        label="Team Name"
                        type="name"
                        id="name"
                        size="small"
                        autoComplete="name"
                        value={temporaryTeam.name}
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
                            onClick={handleTeamDelete}
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


            {/* Modal for CREATE team */}
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
                }}> Create Team</Typography>

                <Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <TextField
                        xs
                        required
                        margin="dense"
                        id="category"
                        label="Category"
                        name="category"
                        autoComplete="category"
                        autoFocus
                        size="small"
                        value={temporaryTeam.category}
                        onChange={handleFormChange}
                        sx={{ mt: 2 }}
                        variant="filled"

                    />
                    <TextField
                        xs
                        required
                        name="name"
                        margin="dense"
                        label="Team Name"
                        type="name"
                        id="name"
                        size="small"
                        autoComplete="name"
                        value={temporaryTeam.name}
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
            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayCreateModal ? "Show" : ""}`}
                onClick={() => { setDisplayCreateModal(!displayCreateModal); clearState(); }}
            />

        </React.Fragment>
    )
}

export default TeamsPage