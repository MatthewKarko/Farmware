import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axiosInstance from '../../axios';
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography, TextField } from "@mui/material"

export const EditProduceSuffix = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const produce = location.state;
    
    const [suffixList, setSuffixList] = useState([]);
    
    useEffect(()=>{
        console.log(produce);
       
        axiosInstance
            .get(`produce/${produce.id}/get_suffixes/`)
            .then((res) => {
                res.data.map((data) => {
                    setSuffixList(suffixList => [...suffixList, data])
                    console.log(res.data);
                })
            })
     
    }, [])

    const handleEditClick = (event, row) => {
        event.preventDefault();
        // setDisplayEditModal(!displayEditModal);

        // axiosInstance.get(`produce/${row.id}`)
        //     .then((res) => {
        //         console.log(res.data);
        //         setProduceObj(res.data);
        //         console.log(JSON.parse(res.data.quantity_suffixes));
        //         setEditProduceSuffix(JSON.parse(res.data.quantity_suffixes));
        //     })
    };

    const handleDeleteClick = (event, row) => {
        event.preventDefault();
        axiosInstance.delete(`produce_quantity_suffix/${row.id}/`)

        
    }


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
                            }}>{produce.name} suffixes</Typography>

                        </Grid>

                        
                    </Grid>
                </Box>

                <TableContainer component={Paper} >
                    <Table aria-label="simple table">
                        <colgroup>
                            <col style={{ width: '20%' }} />
                            <col style={{ width: '65%' }} />
                            <col style={{ width: '5%' }} />
                            <col style={{ width: '5%' }} />
                            <col style={{ width: '5%' }} />
                        </colgroup>
                        <TableHead>
                            <TableRow sx={{
                                "& th": {
                                    fontSize: "1.10rem",
                                }
                            }}>
                                <TableCell className="tableCell">Suffix ID</TableCell>
                                <TableCell className="tableCell">Suffix</TableCell>
                                <TableCell className="tableCell">Base Equivalent</TableCell>
                                <TableCell className="tableCell"></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {suffixList.map((row) => (
                                <TableRow sx={{
                                    "& th": {
                                        fontSize: "1.10rem",
                                    }
                                }} key={row.id} >
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.suffix}</TableCell>
                                    <TableCell className="tableCell">{row.base_equivalent}</TableCell>
                                    <TableCell className="tableCell">
                                        <Button variant="outlined" size="medium"
                                            style={{                                              
                                                width: "100px",
                                            }}
                                            onClick={(event) => handleEditClick(event, row)}
                                        >Edit QS</Button>
                                    </TableCell>
                                    <TableCell className="tableCell">
                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#FF0000",
                                                borderColor: "#FF0000",
                                                margin: "5px",
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
