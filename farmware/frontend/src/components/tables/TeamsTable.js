import React, { useState, useEffect, Fragment } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';

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
            .get(`teams/`, {
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

    const handleEditSubmit = () => {

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

    const handleTeamDelete = () => {
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
                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                }}> Teams Table</Typography>

                <Button type="submit" variant="outlined" size="large" style={{
                    color: "#028357",
                    borderColor: "#028357",
                    margin: "20px",
                }}
                    onClick={() => { setDisplayCreateModal(!displayCreateModal) }}
                >Create Team</Button>
                

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

                <form>
                    <label>Category:</label>
                    <input
                        type="text"
                        name="category"
                        required="required"
                        placeholder="Enter a category..."
                        value={temporaryTeam.category}
                        onChange={handleFormChange}
                        style={{ width: "200px" }}
                    />
                    <br></br>
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        required="required"
                        placeholder="Enter a name..."
                        value={temporaryTeam.name}
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
                        onClick={() => { handleTeamDelete() }}
                    >Delete Team</Button>
                </form>
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
                    margin: "20px",
                }}> Create Team</Typography>

                <form>
                <label>Category:</label>
                    <input
                        type="text"
                        name="category"
                        required="required"
                        placeholder="Enter a category..."
                        value={temporaryTeam.category}
                        onChange={handleFormChange}
                        style={{ width: "200px" }}
                    />
                    <br></br>
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        required="required"
                        placeholder="Enter a name..."
                        value={temporaryTeam.name}
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

export default TeamsPage