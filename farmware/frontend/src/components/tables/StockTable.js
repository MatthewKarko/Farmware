import React, { useState, useEffect, Fragment } from "react";
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography, TextField, FormControl, InputLabel, Select, MenuItem, ListItemText } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import useNotification from "../alert/UseNotification";

function StockTable() {
    const [msg, sendNotification] = useNotification(); //for the success alerts

    const [stockList, setStockList] = useState([]);
    const [produceList, setProduceList] = useState([]);

    const [displayCreateModal, setDisplayCreateModal] = useState(false);

    const [reloadFlag, setReloadFlag] = useState(false);
    const reloadStock = () => {
        setStockList([]);
        setReloadFlag(!reloadFlag); //prompts a reload of stock
    }
    useEffect(() => {
        axiosInstance
            .get(`stock/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setStockList(stockList => [...stockList, data])
                })
            })
            .catch((err) => {
                alert("ERROR: Getting stock failed");
            });

        axiosInstance
            .get(`produce/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setProduceList(produceList => [...produceList, data])
                })
            })
            .catch((err) => {
                alert("ERROR: Getting produce failed");
            });
    }, [reloadFlag]);

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
        setDisplayCreateModal(!displayCreateModal);
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

    const [temporaryProduce, setTemporaryProduce] = useState({
        produceSelected: "",
        suffixSelected: "",
        varietySelected: "",
        produceQuantity: 0,
    });

    const [produceSuffixes, setProduceSuffixes] = useState([]);

    const clearTemporaryProduce = () => {
        const formValues = {
            produceSelected: "",
            suffixSelected: "",
            varietySelected: "",
            produceQuantity: 0,
        };
        setTemporaryProduce({ ...formValues });
    };

    const handleProduceChange = (event) => {
        //clear the temporary produce (since all the fields change)
        clearTemporaryProduce();

        //set new produce
        const newFormData = { ...temporaryProduce };
        newFormData["produceSelected"] = event.target.value;
        setTemporaryProduce({ ...newFormData });

        // Correct the displayed suffix and variety options, and clear any prior stored state.

        //remove all from the suffix state
        let len = produceSuffixes.length
        for (let i = 0; i < len; i++) {
            produceSuffixes.pop();
        }

        //get all the new suffix
        axiosInstance
            .get('/produce/' + event.target.value + '/get_suffixes/', {
            })
            .then((res) => {
                res.data.map((data) => {
                    setProduceSuffixes(produceSuffixes => [...produceSuffixes, data])
                })
            })
            .catch((err) => {
                alert("ERROR: Getting suffixes for produce id failed");
            });

        // //Temporarily, it will switch between two suffix lists to demonstrate functionality
        // if (len == 2) {
        //     for (let i = 0; i < produceSuffixData2.length; i++) {
        //         produceSuffixes.push(produceSuffixData2[i]);
        //     }
        // } else {
        //     for (let i = 0; i < produceSuffixData.length; i++) {
        //         produceSuffixes.push(produceSuffixData[i]);
        //     }
        // }

        //now do same for varieties
        //remove all from the suffix state
        let len_var = produceVarieties.length
        for (let i = 0; i < len_var; i++) {
            produceVarieties.pop();
        }

        //get all the new varieties
        axiosInstance
            .get('/produce/' + event.target.value + '/get_varieties/', {
            })
            .then((res) => {
                res.data.map((data) => {
                    setProduceVarieties(produceVarieties => [...produceVarieties, data])
                })
            })
            .catch((err) => {
                alert("ERROR: Getting suffixes for produce id failed");
            });

        // //Temporarily, it will switch between two varieties lists to demonstrate functionality
        // if (len_var == 2) {
        //     for (let i = 0; i < produceVarietyData2.length; i++) {
        //         produceVarieties.push(produceVarietyData2[i]);
        //     }
        // } else {
        //     for (let i = 0; i < produceVarietyData.length; i++) {
        //         produceVarieties.push(produceVarietyData[i]);
        //     }
        // }
    };

    const handleSuffixChange = (event) => {
        const newFormData = { ...temporaryProduce };
        newFormData["suffixSelected"] = event.target.value;
        setTemporaryProduce({ ...newFormData });
    };

    const [produceVarieties, setProduceVarieties] = useState([]);

    const handleVarietyChange = (event) => {
        const newFormData = { ...temporaryProduce };
        newFormData["varietySelected"] = event.target.value;
        setTemporaryProduce({ ...newFormData });
    };

    const handleFormChange = (event) => {
        event.preventDefault();
        if (!isNaN(+event.target.value)) {
            //is number
            const newFormData = { ...temporaryProduce };
            newFormData["produceQuantity"] = event.target.value;
            setTemporaryProduce({ ...newFormData });
        } else {
            alert("Invalid quantity input.");
        }
    };

    const [displayAddProduceModal, setDisplayAddProduceModal] = useState(false);

    const handleAddProduceSubmit = (event) => {
        event.preventDefault();

        //TO DO: CHECKS FOR VALID INPUT

        //ASSUMING VALID INPUT:
        alert("Submitted a produce add to order.\nProduce ID:" + temporaryProduce.produceSelected + "\nSuffix ID: " + temporaryProduce.suffixSelected + "\nVariety ID: " + temporaryProduce.varietySelected + "\nQuantity: " + temporaryProduce.produceQuantity)

        //CLEAR PRODUCE SELECTED FIELDS
        clearTemporaryProduce();
        setDisplayAddProduceModal(false);
    };

    //This is required to transfer the changes to produce suffix list to the Select menu
    let produceSuffixOptions = null;
    if (produceSuffixes.length != 0) {
        produceSuffixOptions = produceSuffixes.map((suf) => <MenuItem key={suf.id} value={suf.id}>
            <ListItemText primary={suf.suffix} />
        </MenuItem>);
    }

    //This is required to transfer the changes to produce variety list to the Select menu
    let produceVarietyOptions = null;
    if (produceVarieties.length != 0) {
        produceVarietyOptions = produceVarieties.map((variety_val) => <MenuItem key={variety_val.id} value={variety_val.id}>
            <ListItemText primary={variety_val.variety} />
        </MenuItem>);
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

                <TableContainer component={Paper} style={{}}>
                    <Table aria-label="simple table" style={{}}>
                        <colgroup>
                            <col style={{ width: '8%' }} />
                            <col style={{ width: '18%' }} />
                            <col style={{ width: '18%' }} />
                            <col style={{ width: '18%' }} />
                            <col style={{ width: '18%' }} />
                            <col style={{ width: '20%' }} />
                        </colgroup>
                        <TableHead>
                            <TableRow sx={{
                                "& th": {
                                    fontSize: "1.10rem",
                                }
                            }}>
                                <TableCell className="tableCell">ID</TableCell>
                                <TableCell className="tableCell">Produce Name</TableCell>
                                <TableCell className="tableCell">Produce Variety</TableCell>
                                <TableCell className="tableCell">SUFFIX</TableCell>
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
                                    <TableCell className="tableCell">{row.quantity_suffix_name}</TableCell>
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


            {/* Modal for CREATE supplier */}
            <div className={`Modal Large ${displayCreateModal ? "Show" : ""}`}>
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
                }}>Create Stock</Typography>


                <Box component="form" onSubmit={handleAddProduceSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Box noValidate>
                        <FormControl sx={{ width: "300px", mt: 2 }}>
                            <InputLabel id="demo-simple-select-label">Produce</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                // value={temporaryOrder.produce_id}
                                label="Select a Produce"
                                onChange={handleProduceChange}
                                value={temporaryProduce.produceSelected}
                            >
                                {
                                    produceList.map((produce) => {
                                        return (
                                            <MenuItem key={produce.id} value={produce.id}>
                                                <ListItemText primary={produce.name} />
                                            </MenuItem>
                                        )
                                    })
                                }
                            </Select>
                        </FormControl>
                    </Box>

                    <Box noValidate>
                        <FormControl sx={{ width: "300px", mt: 2 }}>
                            <InputLabel id="demo-simple-select-label">Suffix</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                label="Select a Suffix"
                                onChange={handleSuffixChange}
                                value={temporaryProduce.suffixSelected}
                            >
                                {produceSuffixOptions}
                            </Select>
                        </FormControl>
                    </Box>

                    <Box noValidate>
                        <FormControl sx={{ width: "300px", mt: 2 }}>
                            <InputLabel id="demo-simple-select-label">Variety</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                label="Select a Variety"
                                onChange={handleVarietyChange}
                                value={temporaryProduce.varietySelected}
                            >
                                {produceVarietyOptions}
                            </Select>
                        </FormControl>
                    </Box>


                    <TextField
                        required
                        margin="normal"
                        name="produce_qty"
                        label="Produce Quantity"
                        type="produce_qty"
                        id="produce_qty"
                        autoComplete="produce_qty"
                        size="small"
                        value={temporaryProduce.produceQuantity}
                        onChange={handleFormChange}
                        sx={{ width: "300px" }}
                        variant="filled"
                    />

                    <Box noValidate>
                        <Button
                            type="submit"
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Create
                        </Button>
                    </Box>
                </Box>

            </div>

            <div
                className={`Overlay ${displayCreateModal ? "Show" : ""}`}
                onClick={() => { setDisplayCreateModal(!displayCreateModal); }}
            />

        </React.Fragment>
    )



}

export default StockTable;