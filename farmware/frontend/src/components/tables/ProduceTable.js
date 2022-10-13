import React, { useState, useEffect, Fragment } from "react";
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/TableAndModal.css';
import axiosInstance from '../../axios';

function ProduceTable() {

    const [produceList, setProduceList] = useState([]);
    const [displayEditModal, setDisplayEditModal] = useState(false);
    const [displayDeleteModal, setDisplayDeleteModal] = useState(false);
    const [displayCreateModal, setDisplayCreateModal] = useState(false);

    const [tempName, setTempName] = useState("");

    useEffect(() => {
        axiosInstance
            .get(`produce/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setProduceList(produceList => [...produceList, data])
                    console.log(res.data)
                })
            })
            .catch((err) => {
                alert("ERROR: Getting users failed");
            });

    }, []);

    const handleNameChange = (event) => {
        event.preventDefault();
    };

    const handleEditClick = (event, row) => {
        event.preventDefault();
        setDisplayEditModal(!displayEditModal);
    };

    const handleEditSubmit = (event) => {
        event.preventDefault();

    };

    const handleDeleteClick = (event, row) => {
        event.preventDefault();
        setDisplayDeleteModal(!displayDeleteModal);
        //Confirmation modal
    };

    const handleDeleteSubmit = (event, row) => {
        event.preventDefault();
    };

    const handleCreateClick = () => {
        event.preventDefault();
        setDisplayCreateModal(!displayCreateModal);
    };

    const handleCreateSubmit = (event) => {
        event.preventDefault();
    };

    return (
        <React.Fragment>
            <div className="main-content">
                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    paddingBottom: '20px',
                }}>Produce Table</Typography>

                <TableContainer component={Paper} style={{ maxWidth: 800, margin:"auto"}}>
                    <Table aria-label="simple table" style={{ maxWidth: 800, margin:"auto" }}>
                    <colgroup>
                        <col style={{width:'20%'}}/>
                        <col style={{width:'50%'}}/>
                        <col style={{width:'30%'}}/>
                    </colgroup>
                        <TableHead>
                            <TableRow sx={{
                                "& th": {
                                    fontSize: "1.10rem",
                                  }
                            }}>
                                <TableCell className="tableCell">Produce ID</TableCell>
                                <TableCell className="tableCell">Produce Name</TableCell>
                                <TableCell className="tableCell"></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {produceList.map((row) => (
                                <TableRow sx={{
                                    "& th": {
                                        fontSize: "1.10rem",
                                      }
                                }} key={row.id} >
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.name}</TableCell>

                                    <TableCell className="tableCell">
                                        <Button variant="outlined" size="medium"
                                            style={{
                                                margin:"10px",
                                                width: "80px",
                                            }}
                                            onClick={(event) => handleEditClick(event, row)}
                                        >Edit</Button>
                                    
                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#FF0000",
                                                borderColor: "#FF0000",
                                                margin:"10px",
                                                width: "80px",
                                            }}
                                            onClick={(event) => handleDeleteClick(event, row)}
                                        >Delete</Button>
                                    </TableCell>

                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>

                <Box textAlign='center'>
                    <Button variant="outlined" size="large"
                        style={{
                            color: "#028357",
                            borderColor: "#028357",
                            marginTop: "20px",
                        }}
                        onClick={(event) => handleCreateClick()}
                    >Create Produce</Button>
                </Box>

            </div>



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
                }}>Edit Produce</Typography>

                <form onSubmit={handleEditSubmit}>
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        required="required"
                        placeholder="Enter a name..."
                        value={tempName}
                        onChange={handleNameChange}
                        style={{ width: "200px" }}
                    />
                    <br></br>
                    <Button type="submit" variant="outlined" size="large" style={{
                        color: "#028357",
                        borderColor: "#028357",
                    }}
                        onClick={() => setDisplayEditModal(!displayEditModal)}
                    >Submit</Button>
                </form>
            </div>

            <div className={`Modal ${displayCreateModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayCreateModal(!displayCreateModal); setTempName(""); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    margin: "20px",
                }}>Create Produce</Typography>

                <form onSubmit={handleCreateSubmit}>
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        required="required"
                        placeholder="Enter a name..."
                        value={tempName}
                        onChange={handleNameChange}
                        style={{ width: "200px" }}
                    />
                    <br></br>
                    <Button type="submit" variant="outlined" size="large" style={{
                        color: "#028357",
                        borderColor: "#028357",
                    }}
                        onClick={() => setDisplayCreateModal(!displayCreateModal)}
                    >Create</Button>
                </form>
            </div>

            <div className={`Modal ${displayDeleteModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayDeleteModal(!displayEditModal); setTempName(""); }}
                >X</button>

                <Typography variant="h5" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    margin: "20px",
                }}>Are you sure you want to delete the produce?</Typography>
                <Button type="submit" variant="outlined" size="large" style={{
                    color: "#FF0000",
                    borderColor: "#FF0000",
                }}
                    onClick={() => { setDisplayDeleteModal(!displayEditModal); handleDeleteSubmit(); }}
                >Delete</Button>
            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayEditModal ? "Show" : ""}`}
                onClick={() => { setDisplayEditModal(!displayEditModal); setTempName(""); }}
            />
            <div
                className={`Overlay ${displayDeleteModal ? "Show" : ""}`}
                onClick={() => { setDisplayDeleteModal(!displayDeleteModal); setTempName(""); }}
            />
            <div
                className={`Overlay ${displayCreateModal ? "Show" : ""}`}
                onClick={() => { setDisplayCreateModal(!displayCreateModal); setTempName(""); }}
            />
        </React.Fragment>
    )
}

export default ProduceTable