import React, { useState, useEffect, Fragment } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/TableAndModal.css';
import axiosInstance from '../../axios';

function ProduceTable() {

    const [produceList, setProduceList] = useState([]);
    const [displayEditModal, setDisplayEditModal] = useState(false);
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

    const handleEditClick = (event, row) => {
        event.preventDefault();
        setDisplayEditModal(!displayEditModal);
      };

      const handleDeleteClick = (event, row) => {
        event.preventDefault();

        //Confirmation modal?
      };
    
      const handleNameChange = (event) => {
        event.preventDefault();
    
      };
    
      const handleEditSubmit = (event) => {
        event.preventDefault();
    
      };


    return (
        <React.Fragment>
            <div className="main-content">
                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                }}>Produce Table</Typography>
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell className="tableCell">ID</TableCell>
                                <TableCell className="tableCell">Produce Name</TableCell>
                                <TableCell className="tableCell">Edit</TableCell>
                                <TableCell className="tableCell">Delete</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {produceList.map((row) => (
                                <TableRow key={row.id}>
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.name}</TableCell>

                                    <TableCell className="tableCell">
                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#028357",
                                                borderColor: "#028357",
                                            }}
                                            onClick={(event) => handleEditClick(event, row)}
                                        >Edit</Button>
                                    </TableCell>

                                        <TableCell className="tableCell">
                                            <Button variant="outlined" size="medium"
                                                style={{
                                                    color: "#FF0000",
                                                    borderColor: "#FF0000",
                                                }}
                                                onClick={(event) => handleDeleteClick(event, row)}
                                            >Delete</Button>
                                        </TableCell>

                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>

            {/* The modal is currently not in MUI components, might change it to MUI later */}
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

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayEditModal ? "Show" : ""}`}
                onClick={() => { setDisplayEditModal(!displayEditModal); clearState(); }}
            />
        </React.Fragment>
    )
}

export default ProduceTable