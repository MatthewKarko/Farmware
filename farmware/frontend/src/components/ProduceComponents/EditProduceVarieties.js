import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axiosInstance from '../../axios';
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography, TextField } from "@mui/material"

export const EditProduceVarieties = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const produce = location.state;
    
    const [varietyList, setVarietyList] = useState([]);
    const [currentVariety, setCurrentVariety] = useState([]);
    const [displayEditModal, setDisplayEditModal] = useState(false);
    const [displayCreateModal, setDisplayCreateModal] = useState(false);
    const [reloadFlag, setReloadFlag] = useState(false);
    const reloadVarieties = () => {
      setVarietyList([]);
      setCurrentVariety([]);
      setReloadFlag(!reloadFlag); //prompts a reload of customers
    }

    useEffect(()=>{
        console.log(produce);
       
        axiosInstance
            .get(`produce/${produce.id}/get_varieties/`)
            .then((res) => {
                res.data.map((data) => {
                    setVarietyList(varietyList => [...varietyList, data])
                    console.log(res.data);
                })
            })
     
    }, [reloadFlag])

    const handleCreateClick = (event) => {
        event.preventDefault();
        setDisplayCreateModal(!displayCreateModal);
    }
    const handleEditClick = (event, row) => {
        event.preventDefault();
        setDisplayEditModal(!displayEditModal);

        axiosInstance.get(`produce_variety/${row.id}/`)
            .then((res) => {
                console.log(res.data);
                setCurrentVariety(res.data);
            })
    };

    const handleFormChange = (evt) => {
        evt.preventDefault();
        const value = evt.target.value;
        setCurrentVariety({
          ...currentVariety,
          [evt.target.name]: value
    });
    
    }
    const handleDeleteClick = (event, row) => {
        event.preventDefault();
        
        axiosInstance.delete(`produce_variety/${row.id}/`)
        reloadVarieties();
        
    }

    const handleVarietyCreateSubmit = (event) => {
        event.preventDefault();

        var postObject = {
            variety: currentVariety.variety,
            produce_id: produce.id,
        }

        axiosInstance
            .post(`produce_variety/`, postObject)
            .catch((err) => console.log(err));
        reloadVarieties();
    }

    const handleVarietyEditSubmit = (event) =>{
        event.preventDefault();

        var postObject = {
            variety: currentVariety.variety,
        }

        axiosInstance
            .patch(`produce_variety/${currentVariety.id}/`, postObject)
            .catch((err) => console.log(err));

        setDisplayEditModal(!displayEditModal);
        reloadVarieties();
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
                            }}>{produce.name} varieties</Typography>

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
                            >Create Variety</Button>
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
                                <TableCell className="tableCell">Variety ID</TableCell>
                                <TableCell className="tableCell">Variety</TableCell>
                                <TableCell className="tableCell"></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {varietyList.map((row) => (
                                <TableRow sx={{
                                    "& th": {
                                        fontSize: "1.10rem",
                                    }
                                }} key={row.id} >
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.variety}</TableCell>
                                    <TableCell className="tableCell">
                                        <Button variant="outlined" size="medium"
                                            style={{                                              
                                                width: "100px",
                                            }}
                                            onClick={(event) => handleEditClick(event, row)}
                                        >Edit Variety</Button>
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
                }}>Produce Variety</Typography>
                <Box component="form" onSubmit={handleVarietyEditSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <TextField
                        InputLabelProps={{ shrink: !! currentVariety.variety }}
                        xs
                        required
                        margin="dense"
                        id="variety"
                        label="Produce Variety"
                        name="variety"
                        autoComplete="variety"
                        autoFocus
                        size="small"
                        value={currentVariety.variety}
                        onChange={handleFormChange}
                        variant="filled"

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
                }}>Produce Variety</Typography>
                <Box component="form" onSubmit={handleVarietyCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <TextField
                        InputLabelProps={{ shrink: !! currentVariety.variety }}
                        xs
                        required
                        margin="dense"
                        id="variety"
                        label="Produce Variety"
                        name="variety"
                        autoComplete="variety"
                        autoFocus
                        size="small"
                        value={currentVariety.variety}
                        onChange={handleFormChange}
                        variant="filled"

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
