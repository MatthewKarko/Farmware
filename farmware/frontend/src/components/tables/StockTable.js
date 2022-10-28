import React, { useState, useEffect, Fragment } from "react";
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography, TextField, FormControl, InputLabel, Select, MenuItem, ListItemText } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import useNotification from "../alert/UseNotification";
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';

function StockTable() {
    const [msg, sendNotification] = useNotification(); //for the success alerts

    const [stockList, setStockList] = useState([]);
    const [produceList, setProduceList] = useState([]);
    const [areaCodesList, setAreaCodeList] = useState([]);
    const [supplierList, setSupplierList] = useState([]);

    const [displayCreateModal, setDisplayCreateModal] = useState(false);

    const [reloadFlag, setReloadFlag] = useState(false);
    const reloadStock = () => {
        setStockList([]);
        setProduceList([]);
        setAreaCodeList([]);
        setSupplierList([]);
        setReloadFlag(!reloadFlag);
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

        axiosInstance
            .get(`area_code/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setAreaCodeList(areaCodeList => [...areaCodeList, data])
                })
            })
            .catch((err) => {
                alert("ERROR: Getting area codes failed");
            });

        axiosInstance
            .get(`supplier/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setSupplierList(supplierList => [...supplierList, data])
                })
            })
            .catch((err) => {
                alert("ERROR: Getting suppliers failed");
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
        axiosInstance
            .delete('stock/' + row.id + '/', {
            })
            .catch((err) => {
                alert("ERROR: Failed to delete stock");
            });
        reloadStock();
        sendNotification({ msg: 'Success: Stock Deleted', variant: 'success' });
    };

    const [temporaryStock, setTemporaryStock] = useState({
        produce_id: "",
        quantity_suffix_id: "",
        variety_id: "",
        quantity: "",
        supplier_id: "",
        area_code_id: "",
        date_seeded: "",
        date_planted: "",
        date_picked: "",
        ehd: "",
        base_equivalent: ""
    });

    const [produceSuffixes, setProduceSuffixes] = useState([]);

    const clearTemporaryStock = () => {
        const formValues = {
            produce_id: "",
            quantity_suffix_id: "",
            variety_id: "",
            quantity: "",
            supplier_id: "",
            area_code_id: "",
            date_seeded: "",
            date_planted: "",
            date_picked: "",
            ehd: "",
            base_equivalent: ""
        };
        setTemporaryStock({ ...formValues });
    };

    const handleProduceChange = (event) => {
        //clear the fields that relate to produce. And set produce to new value.
        const newFormData = { ...temporaryStock };
        newFormData["produce_id"] = event.target.value;
        newFormData["quantity_suffix_id"] = "";
        newFormData["variety_id"] = "";
        newFormData["quantity"] = "";
        setTemporaryStock({ ...newFormData });


        //set new produce
        // const newFormData = { ...temporaryProduce };
        // newFormData["produce_id"] = event.target.value;
        // setTemporaryProduce({ ...newFormData });

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
    };

    const handleSuffixChange = (event) => {
        const newFormData = { ...temporaryStock };
        newFormData["quantity_suffix_id"] = event.target.value;
        //going to need to get the base_equivalent from the event.target.value 
        let base_equivalent = 0;
        for (let i = 0; i < produceSuffixes.length; i++) {
            if (produceSuffixes[i].id == event.target.value) {
                console.log("found suffix");
                base_equivalent = produceSuffixes[i].base_equivalent;
            }
        }
        newFormData["base_equivalent"] = base_equivalent;
        setTemporaryStock({ ...newFormData });
    };

    const [produceVarieties, setProduceVarieties] = useState([]);

    const handleVarietyChange = (event) => {
        const newFormData = { ...temporaryStock };
        newFormData["variety_id"] = event.target.value;
        setTemporaryStock({ ...newFormData });
    };

    const handleFormChange = (event) => {
        event.preventDefault();
        if (event.target.value.length == 0) {
            const newFormData = { ...temporaryStock };
            newFormData["quantity"] = "";
            setTemporaryStock({ ...newFormData });
            return;
        }
        const parsed = parseInt(event.target.value, 10);
        if (isNaN(parsed)) {
            alert("Invalid quantity input.");
        } else {
            const newFormData = { ...temporaryStock };
            newFormData["quantity"] = parsed;
            setTemporaryStock({ ...newFormData });
        }
    };

    const handleStockCreateSubmit = (event) => {
        event.preventDefault();

        //send off the request
        var postObject = {
            produce_id: temporaryStock.produce_id,
            quantity_suffix_id: temporaryStock.quantity_suffix_id,
            variety_id: temporaryStock.variety_id,
            quantity: temporaryStock.quantity,
            supplier_id: temporaryStock.supplier_id,
            area_code_id: temporaryStock.area_code_id,
        }
        if (temporaryStock.date_seeded != "") {
            postObject['date_seeded'] = temporaryStock.date_seeded;
        }
        if (temporaryStock.date_picked != "") {
            postObject['date_picked'] = temporaryStock.date_picked;
        }
        if (temporaryStock.date_planted != "") {
            postObject['date_planted'] = temporaryStock.date_planted;
        }
        if (temporaryStock.ehd != "") {
            postObject['ehd'] = temporaryStock.ehd;
        }

        console.log(postObject);

        axiosInstance.post(`stock/`, postObject)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });

        clearTemporaryStock();

        //TO DO: CHECKS FOR VALID INPUT

        setDisplayCreateModal(false);

        reloadStock();

        setPickedDateValue(null);
        setPlantedDateValue(null);
        setSeededDateValue(null);
        setEHD(null);

        sendNotification({ msg: 'Success: Stock Created', variant: 'success' });
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


    const handleSupplierChange = (event) => {
        event.preventDefault();
        const newFormData = { ...temporaryStock };
        newFormData["supplier_id"] = event.target.value;
        setTemporaryStock({ ...newFormData });
    }

    const handleAreaCodeChange = (event) => {
        event.preventDefault();
        const newFormData = { ...temporaryStock };
        newFormData["area_code_id"] = event.target.value;
        setTemporaryStock({ ...newFormData });
    }

    const [seededDateValue, setSeededDateValue] = useState("");
    const handleSeededDateChange = (newValue) => {
        setSeededDateValue(dayjs(newValue).format('YYYY-MM-DD')); //set value for the date input field
        const newFormData = { ...temporaryStock };
        newFormData["date_seeded"] = dayjs(newValue).format('YYYY-MM-DD');
        setTemporaryStock({ ...newFormData });
    };

    const [plantedDateValue, setPlantedDateValue] = useState("");
    const handlePlantedDateChange = (newValue) => {
        setPlantedDateValue(dayjs(newValue).format('YYYY-MM-DD')); //set value for the date input field
        const newFormData = { ...temporaryStock };
        newFormData["date_planted"] = dayjs(newValue).format('YYYY-MM-DD');
        setTemporaryStock({ ...newFormData });
    };

    const [pickedDateValue, setPickedDateValue] = useState("");
    const handlePickedDateChange = (newValue) => {
        setPickedDateValue(dayjs(newValue).format('YYYY-MM-DD')); //set value for the date input field
        const newFormData = { ...temporaryStock };
        newFormData["date_picked"] = dayjs(newValue).format('YYYY-MM-DD');
        setTemporaryStock({ ...newFormData });
    };

    const [ehd, setEHD] = useState("");
    const handleEHD = (newValue) => {
        console.log(dayjs(newValue).format('YYYY-MM-DD').toString());
        setEHD(dayjs(newValue).format('YYYY-MM-DD').toString()); //set value for the date input field
        const newFormData = { ...temporaryStock };
        newFormData["ehd"] = dayjs(newValue).format('YYYY-MM-DD');
        setTemporaryStock({ ...newFormData });
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

                <TableContainer component={Paper} style={{}}>
                    <Table aria-label="simple table" style={{}}>
                        <colgroup>
                            <col style={{ width: '4%' }} />
                            <col style={{ width: '14%' }} />
                            <col style={{ width: '14%' }} />
                            <col style={{ width: '14%' }} />
                            <col style={{ width: '14%' }} />
                            <col style={{ width: '15%' }} />
                            <col style={{ width: '22%' }} />
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
                                <TableCell className="tableCell">Produce Suffix</TableCell>
                                <TableCell className="tableCell">Stock Quantity</TableCell>
                                <TableCell className="tableCell">Quantity Available</TableCell>
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
                                    <TableCell className="tableCell">{row.quantity_available}</TableCell>
                                    <TableCell className="tableCell">

                                    <Button variant="outlined" size="medium"
                                            style={{
                                                margin: "10px",
                                                width: "90px",
                                            }}
                                            onClick={(event) => handleDatesClick(event, row)}
                                        >Dates</Button>

                                        <Button variant="outlined" size="medium"
                                            style={{
                                                margin: "10px",
                                                width: "90px",
                                            }}
                                            onClick={(event) => handleEditClick(event, row)}
                                        >Edit</Button>

                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#FF0000",
                                                borderColor: "#FF0000",
                                                margin: "10px",
                                                width: "90px",
                                            }}
                                            onClick={(event) => handleDeleteClick(event, row)}
                                        >Delete</Button>

                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#028357",
                                                borderColor: "#028357",
                                                width: "90px",
                                                margin: "10px",
                                            }}
                                            onClick={(event) => handleCompleteClick(event,row)}
                                        >Complete</Button>

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


                <Box component="form" onSubmit={handleStockCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <Box noValidate>
                        <FormControl sx={{ width: "200px", mt: 2 }} required>
                            <InputLabel id="demo-simple-select-label">Supplier</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                // value={temporaryOrder.produce_id}
                                label="Select a Supplier"
                                onChange={handleSupplierChange}
                                value={temporaryStock.supplier_id}
                                sx={{ height: "55px" }}
                            >
                                {
                                    supplierList.map((supplier) => {
                                        return (
                                            <MenuItem key={supplier.id} value={supplier.id}>
                                                <ListItemText primary={supplier.name} />
                                            </MenuItem>
                                        )
                                    })
                                }
                            </Select>
                        </FormControl>

                        <FormControl sx={{ width: "200px", mt: 2, ml: 2 }} required>
                            <InputLabel id="demo-simple-select-label">Area Code</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                // value={temporaryOrder.produce_id}
                                label="Select an Area Code"
                                onChange={handleAreaCodeChange}
                                value={temporaryStock.area_code_id}
                                sx={{ height: "55px" }}
                            >
                                {
                                    areaCodesList.map((areaCode) => {
                                        return (
                                            <MenuItem key={areaCode.id} value={areaCode.id}>
                                                <ListItemText primary={areaCode.area_code} />
                                            </MenuItem>
                                        )
                                    })
                                }
                            </Select>
                        </FormControl>
                    </Box>

                    <Box noValidate>
                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DesktopDatePicker
                                label="Date Seeded"
                                name="seeded_date"
                                inputFormat="DD/MM/YYYY"
                                value={seededDateValue || null}
                                onChange={handleSeededDateChange}
                                renderInput={(params) => <TextField {...params} sx={{ width: "230px", mt: 2 }} />}
                            />
                        </LocalizationProvider>

                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DesktopDatePicker
                                label="Date Planted"
                                name="planted_date"
                                inputFormat="DD/MM/YYYY"
                                value={plantedDateValue || null}
                                onChange={handlePlantedDateChange}
                                renderInput={(params) => <TextField {...params} sx={{ width: "230px", mt: 2, ml: 2 }} />}
                            />
                        </LocalizationProvider>

                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DesktopDatePicker
                                label="Date Picked"
                                name="date_picked"
                                inputFormat="DD/MM/YYYY"
                                value={pickedDateValue || null}
                                onChange={handlePickedDateChange}
                                renderInput={(params) => <TextField {...params} sx={{ width: "230px", mt: 2, ml: 2 }} />}
                            />
                        </LocalizationProvider>

                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DesktopDatePicker
                                label="Earliest Harvest Date"
                                name="ehd"
                                inputFormat="DD/MM/YYYY"
                                value={ehd || null}
                                onChange={handleEHD}
                                renderInput={(params) => <TextField {...params} sx={{ width: "230px", mt: 2, ml: 2 }} />}
                            />
                        </LocalizationProvider>


                    </Box>


                    <Box noValidate>
                        <FormControl sx={{ width: "200px", mt: 2 }} required>
                            <InputLabel id="demo-simple-select-label">Produce</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                // value={temporaryOrder.produce_id}
                                label="Select a Produce"
                                onChange={handleProduceChange}
                                value={temporaryStock.produce_id}
                                sx={{ height: "55px" }}
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

                        <FormControl sx={{ width: "200px", mt: 2, ml: 2 }} required>
                            <InputLabel id="demo-simple-select-label">Produce Suffix</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                label="Select a Suffix"
                                onChange={handleSuffixChange}
                                value={temporaryStock.quantity_suffix_id}
                                sx={{ height: "55px" }}
                            >
                                {produceSuffixOptions}
                            </Select>
                        </FormControl>

                        <FormControl sx={{ width: "200px", mt: 2, ml: 2 }} required>
                            <InputLabel id="demo-simple-select-label">Produce Variety</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                label="Select a Variety"
                                onChange={handleVarietyChange}
                                value={temporaryStock.variety_id}
                                sx={{ height: "55px" }}
                            >
                                {produceVarietyOptions}
                            </Select>
                        </FormControl>
                    </Box>

                    <Typography sx={{ mt: 2 }}>Base Equivalent: {temporaryStock.base_equivalent}</Typography>

                    <Box noValidate>
                        {/* <FormControl sx={{ width: "200px", mt: 5 }}>
                        </FormControl> */}

                        <FormControl sx={{ width: "200px" }}>
                            <TextField
                                required
                                margin="normal"
                                name="produce_qty"
                                label="Stock Quantity"
                                type="produce_qty"
                                id="produce_qty"
                                autoComplete="produce_qty"
                                size="small"
                                value={temporaryStock.quantity}
                                onChange={handleFormChange}
                                sx={{ width: "200px" }}
                                variant="filled"
                            />
                        </FormControl>
                    </Box>

                    <Box noValidate>
                        <Button
                            type="submit"
                            variant="contained"
                            sx={{ mt: 2, mb: 2 }}
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