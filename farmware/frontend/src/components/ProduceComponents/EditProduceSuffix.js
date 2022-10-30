import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axiosInstance from '../../axios';
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography, TextField } from "@mui/material"

export const EditProduceSuffix = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [displayEditModal, setDisplayEditModal] = useState(false);
    const [displayCreateModal, setDisplayCreateModal] = useState(false);
    const [produceSuffixObj, setProduceSuffixObj] = useState([]);
    const produce = location.state;
    
    const [suffixList, setSuffixList] = useState([]);
    
    const [reloadFlag, setReloadFlag] = useState(false);
    const reloadSuffixes = () => {
      setProduceSuffixObj([]);
      setSuffixList([]);
      setReloadFlag(!reloadFlag); //prompts a reload of customers
    }
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
     
    }, [reloadFlag])

    const handleFormChange = (evt) => {
        evt.preventDefault();
        const value = evt.target.value;
        setProduceSuffixObj({
          ...produceSuffixObj,
          [evt.target.name]: value
    });
    }
    const handleProduceSuffixSubmit = (event) => {
        event.preventDefault();

        var postObject = {
            suffix: produceSuffixObj.suffix,
            base_equivalent: parseInt(produceSuffixObj.base_equivalent),
        }
        axiosInstance 
            .patch(`produce_quantity_suffix/${produceSuffixObj.id}/`, postObject)
            .then((res) => console.log(res))
        
        setDisplayEditModal(!displayEditModal);
        reloadSuffixes();
    }

    const handleEditClick = (event, row) => {
        event.preventDefault();
        setDisplayEditModal(!displayEditModal);

        axiosInstance.get(`produce_quantity_suffix/${row.id}`)
            .then((res) => {
                console.log(res.data);
                setProduceSuffixObj(res.data);
            })
    };

    const handleDeleteClick = (event, row) => {
        event.preventDefault();
        axiosInstance.delete(`produce_quantity_suffix/${row.id}/`)
        reloadSuffixes();
        
    };

    const handleCreateClick = (event) =>{
        event.preventDefault();
        setDisplayCreateModal(!displayCreateModal);
    }
    const handleCreateSubmit = (event) =>{
        event.preventDefault();
        // setDisplayCreateModal(!displayCreateModal);
        var postObject = {
            produce_id: produce.id,
            suffix: produceSuffixObj.suffix,
            base_equivalent: parseInt(produceSuffixObj.base_equivalent),
        };
        setDisplayCreateModal(!displayCreateModal);
        reloadSuffixes();
        axiosInstance.post(`produce_quantity_suffix/`, postObject).then((res) => console.log(res.data)).catch((err)=> console.log(err));
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
                        <Grid item xs={6} sx={{ textAlign: "right" }}>
                            {/* <Box textAlign='center'> */}
                            <Button variant="outlined" size="large"
                                style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    marginTop: "20px",
                                }}
                                onClick={(event) => handleCreateClick(event)}
                            >Create Suffix</Button>
                        </Grid>

                        
                    </Grid>
                </Box>

                <TableContainer component={Paper} >
                    <Table aria-label="simple table">
                        <colgroup>
                            <col style={{ width: '10%' }} />
                            <col style={{ width: '15%' }} />
                            <col style={{ width: '55%' }} />
                            <col style={{ width: '10%' }} />
                            <col style={{ width: '20%' }} />
                         
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
                                        >Edit Suffix</Button>
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

            <div className={`Modal ${displayEditModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayEditModal(!displayEditModal); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>Produce Suffix</Typography>
                <Box component="form" onSubmit={handleProduceSuffixSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <TextField
                        InputLabelProps={{ shrink: !! produceSuffixObj.suffix }}
                        xs
                        required
                        margin="dense"
                        id="suffix"
                        label="Produce Suffix"
                        name="suffix"
                        autoComplete="suffix"
                        autoFocus
                        size="small"
                        value={produceSuffixObj.suffix}
                        onChange={handleFormChange}
                        variant="filled"

                    /> 
                    <TextField
                        InputLabelProps={{ shrink: !! produceSuffixObj.base_equivalent}}
                        xs
                        required
                        InputProps={{ inputProps: { min: 1, max:100 } }}
                        margin="dense"
                        id="produce_suffix"
                        label="Suffix base equivalent"
                        name="base_equivalent"
                        autoComplete="base_equivalent"
                        autoFocus
                        size="medium"
                        type="number"
                        value={produceSuffixObj.base_equivalent}
                        onChange={handleFormChange}
                        variant="filled"
                        sx={{width: "150px"}}

                    />   

                    <Button
                        type="submit"
                        variant="contained"
                        sx={{ mt: 3, mb: 2, bgcolor: 'green' }}
                    >
                        Submit
                    </Button>
                </Box>             
            </div>

            <div className={`Modal ${displayCreateModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayCreateModal(!displayCreateModal); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>Produce Suffix</Typography>
                <Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <TextField
                        InputLabelProps={{ shrink: !! produceSuffixObj.suffix }}
                        xs
                        required
                        margin="dense"
                        id="suffix"
                        label="Produce Suffix"
                        name="suffix"
                        autoComplete="suffix"
                        autoFocus
                        size="small"
                        value={produceSuffixObj.suffix}
                        onChange={handleFormChange}
                        variant="filled"

                    /> 
                    <TextField
                        InputLabelProps={{ shrink: !! produceSuffixObj.base_equivalent}}
                        xs
                        required
                        InputProps={{ inputProps: { min: 1, max:100 } }}
                        margin="dense"
                        id="produce_suffix"
                        label="Suffix base equivalent"
                        name="base_equivalent"
                        autoComplete="base_equivalent"
                        autoFocus
                        size="medium"
                        type="number"
                        value={produceSuffixObj.base_equivalent}
                        onChange={handleFormChange}
                        variant="filled"
                        sx={{width: "150px"}}

                    />   

                    <Button
                        type="submit"
                        variant="contained"
                        sx={{ mt: 3, mb: 2, bgcolor: 'green' }}
                    >
                        Create
                    </Button>
                </Box>             
            </div>

            <div
                className={`Overlay ${displayEditModal ? "Show" : ""}`}
                onClick={() => { setDisplayEditModal(!displayEditModal); }}
            />
            <div
                className={`Overlay ${displayCreateModal ? "Show" : ""}`}
                onClick={() => { setDisplayCreateModal(!displayCreateModal); }}
            />

        </React.Fragment>
    )
}
