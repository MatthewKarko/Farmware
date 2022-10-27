import React, { useState, useEffect, Fragment } from "react";
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography, TextField } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';

function StockTable() {
    const [org, setOrg] = useState(-1);
    const [stockList, setStockList] = useState([]);

    useEffect(() => {
    axiosInstance
        .get(`user/me/`, {
        })
        .then((res) => {
          // console.log(res.data);
          setOrg(res.data.organisation);
        })
        .catch((err) => {
          alert("ERROR: user/me failed");
    });
    }, []);

    const handleEditClick = (event, row) => {
        event.preventDefault();
        setDisplayEditModal(!displayEditModal);

        // axiosInstance.get(`produce/${row.id}`)
        //     .then((res) => {
        //         console.log(res.data);
        //         setProduceObj(res.data);
        //         console.log(JSON.parse(res.data.quantity_suffixes));
        //         setEditProduceSuffix(JSON.parse(res.data.quantity_suffixes));
        //     })
    };
    const handleCreateClick = () => {
        // event.preventDefault();
        // setDisplayCreateModal(!displayCreateModal);
    };

    const handleEditSubmit = (event) => {
        event.preventDefault();

    };

    const handleDeleteClick = (event, row) => {
        event.preventDefault();
        // setDisplayDeleteModal(!displayDeleteModal);


        // axiosInstance.delete(`produce/${row.id}/`);
        //Confirmation modal
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
                                paddingBottom: '20px',
                            }}>Stock Table</Typography>

                        </Grid>

                        <Grid item xs={6} sx={{ textAlign: "right" }}>
                            {/* <Box textAlign='center'> */}
                            <Button variant="outlined" size="large"
                                style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    marginTop: "20px",
                                }}
                                onClick={(event) => handleCreateClick()}
                            >Add Stock</Button>
                        </Grid>
                    </Grid>
                </Box>

                <TableContainer component={Paper} style={{ }}>
                    <Table aria-label="simple table" style={{}}>
                        <colgroup>
                            <col style={{ width: '15%' }} />
                            <col style={{ width: '20%' }} />
                            <col style={{ width: '30%' }} />
                            <col style={{ width: '15%' }} />
                            <col style={{ width: '20%' }} />
                        </colgroup>
                        <TableHead>
                            <TableRow sx={{
                                "& th": {
                                    fontSize: "1.10rem",
                                }
                            }}>
                                <TableCell className="tableCell">Stock ID</TableCell>
                                <TableCell className="tableCell">Produce Name</TableCell>
                                <TableCell className="tableCell">Produce Variety</TableCell>
                                <TableCell className="tableCell">Stock Quantity</TableCell>
                                <TableCell className="tableCell"></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {stockList.map((row) => (
                                <TableRow sx={{
                                    "& th": {
                                        fontSize: "1.10rem",
                                    }
                                }} key={row.id} >
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.produce_name}</TableCell>
                                    <TableCell className="tableCell">{row.variety_name}</TableCell>
                                    <TableCell className="tableCell">{row.quantity}</TableCell>
                                    <TableCell className="tableCell">
                                        <Button variant="outlined" size="medium"
                                            style={{
                                                margin: "10px",
                                                width: "80px",
                                            }}
                                            onClick={(event) => handleEditClick(event, row)}
                                        >Edit</Button>

                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#FF0000",
                                                borderColor: "#FF0000",
                                                margin: "10px",
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

            </div>

        </React.Fragment>
        )



}

export default StockTable;