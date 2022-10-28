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
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import PendingActionsIcon from '@mui/icons-material/PendingActions';

function StockTable() {
    const [msg, sendNotification] = useNotification(); //for the success alerts

    const [stockList, setStockList] = useState([]);
    const [produceList, setProduceList] = useState([]);
    const [areaCodesList, setAreaCodeList] = useState([]);
    const [supplierList, setSupplierList] = useState([]);

    const [displayCreateModal, setDisplayCreateModal] = useState(false);
    const [displayEditModal, setDisplayEditModal] = useState(false);

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

    const [edittingStockID, setEdittingStockID] = useState(-1);
    const handleEditClick = (event, row) => {
        event.preventDefault();
        clearTemporaryStock(); //empty it first

        setEdittingStockID(row.id);
        //need to fill the varieties and suffixes list by query
        setSuffixesForProduceID(row.produce_id);
        setVarieitesForProduceID(row.produce_id);

        //set the date values in the input fields:
        if (row.date_seeded != null && row.date_seeded != "") {
            setSeededDateValue(dayjs(row.date_seeded).format('YYYY-MM-DD'));
        }
        if (row.date_planted != null && row.date_planted != "") {
            setPlantedDateValue(dayjs(row.date_planted).format('YYYY-MM-DD')); //set value for the date input field
        }
        if (row.date_picked != null && row.date_picked != "") {
            setPickedDateValue(dayjs(row.date_picked).format('YYYY-MM-DD')); //set value for the date input field
        }
        if (row.ehd != null && row.ehd != "") {
            setEHD(dayjs(row.ehd).format('YYYY-MM-DD')); //set value for the date input field
        }

        const formValues = {
            produce_id: row.produce_id,
            quantity_suffix_id: row.quantity_suffix_id,
            variety_id: row.variety_id,
            quantity: row.quantity,
            supplier_id: row.supplier_id,
            area_code_id: row.area_code_id,
            date_seeded: row.date_seeded,
            date_planted: row.date_planted,
            date_picked: row.date_picked,
            ehd: row.ehd,
            base_equivalent: row.base_equivalent,
            quantity_available: row.quantity_available
        };
        setTemporaryStock({ ...formValues });

        setDisplayEditModal(true);
    };

    const handleCreateClick = () => {
        setDisplayCreateModal(!displayCreateModal);
    };

    const handleEditSubmit = (event) => {
        event.preventDefault();

        //VALIDATE INPUTS
        let ret = createStockObjectAndValidateInputs();
        if (ret == null) {
            return; //alert already dislayed
        }

        //otherwise, send edit request
        axiosInstance.put('stock/' + edittingStockID + '/', ret)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });

        setDisplayEditModal(false);

        reloadStock();
        sendNotification({ msg: 'Success: Stock Updated', variant: 'success' });
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
        date_seeded: null,
        date_planted: null,
        date_picked: null,
        ehd: null,
        base_equivalent: "",
        quantity_available: ""
    });

    const [produceSuffixes, setProduceSuffixes] = useState([]);

    const clearTemporaryStock = () => {
        //reset the date values
        setSeededDateValue(null); //set value for the date input field
        setPlantedDateValue(null); //set value for the date input field
        setPickedDateValue(null); //set value for the date input field
        setEHD(null); //set value for the date input field

        const formValues = {
            produce_id: "",
            quantity_suffix_id: "",
            variety_id: "",
            quantity: "",
            supplier_id: "",
            area_code_id: "",
            date_seeded: null,
            date_planted: null,
            date_picked: null,
            ehd: null,
            base_equivalent: "",
            quantity_available: ""
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
        newFormData["base_equivalent"] = "";
        newFormData["quantity_available"] = "";
        setTemporaryStock({ ...newFormData });

        // Correct the displayed suffix and variety options, and clear any prior stored state.
        setSuffixesForProduceID(event.target.value);
        setVarieitesForProduceID(event.target.value);
    };

    function setSuffixesForProduceID(produce_id) {
        //remove all from the suffix state
        let len = produceSuffixes.length
        for (let i = 0; i < len; i++) {
            produceSuffixes.pop();
        }

        //get all the new suffix
        axiosInstance
            .get('/produce/' + produce_id + '/get_suffixes/', {
            })
            .then((res) => {
                res.data.map((data) => {
                    setProduceSuffixes(produceSuffixes => [...produceSuffixes, data])
                })
            })
            .catch((err) => {
                alert("ERROR: Getting suffixes for produce id failed");
            });
    }

    function setVarieitesForProduceID(produce_id) {
        let len_var = produceVarieties.length
        for (let i = 0; i < len_var; i++) {
            produceVarieties.pop();
        }

        //get all the new varieties
        axiosInstance
            .get('/produce/' + produce_id + '/get_varieties/', {
            })
            .then((res) => {
                res.data.map((data) => {
                    setProduceVarieties(produceVarieties => [...produceVarieties, data])
                })
            })
            .catch((err) => {
                alert("ERROR: Getting suffixes for produce id failed");
            });
    }

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
        //reset the base equivalent
        newFormData["base_equivalent"] = base_equivalent;
        setTemporaryStock({ ...newFormData });
    };

    const [produceVarieties, setProduceVarieties] = useState([]);

    const handleVarietyChange = (event) => {
        const newFormData = { ...temporaryStock };
        newFormData["variety_id"] = event.target.value;
        setTemporaryStock({ ...newFormData });
    };

    const handleQuantityChange = (event) => {
        event.preventDefault();
        const newFormData = { ...temporaryStock };
        newFormData["quantity"] = event.target.value;
        setTemporaryStock({ ...newFormData });
    };

    const handleQuantityAvailableChange = (event) => {
        event.preventDefault();
        const newFormData = { ...temporaryStock };
        newFormData["quantity_available"] = event.target.value;
        setTemporaryStock({ ...newFormData });
    };

    function createStockObjectAndValidateInputs() {
        //send off the request
        var postObject = {
            produce_id: temporaryStock.produce_id,
            quantity_suffix_id: temporaryStock.quantity_suffix_id,
            variety_id: temporaryStock.variety_id,
            quantity: temporaryStock.quantity,
            supplier_id: temporaryStock.supplier_id,
            area_code_id: temporaryStock.area_code_id,
        }
        if (temporaryStock.date_seeded != null && temporaryStock.date_seeded != "") {
            postObject['date_seeded'] = temporaryStock.date_seeded;
        }
        if (temporaryStock.date_picked != null && temporaryStock.date_picked != "") {
            postObject['date_picked'] = temporaryStock.date_picked;
        }
        if (temporaryStock.date_planted != null && temporaryStock.date_planted != "") {
            postObject['date_planted'] = temporaryStock.date_planted;
        }
        if (temporaryStock.ehd != null && temporaryStock.ehd != "") {
            postObject['ehd'] = temporaryStock.ehd;
        }

        //CHECKS FOR INPUT
        let temp_str = "Error! The following fields are required:\n"
        let initial_len = temp_str.length;

        if (temporaryStock.supplier_id == "") {
            temp_str += "Supplier, "
        }
        if (temporaryStock.area_code_id == "") {
            temp_str += "Area Code, "
        }
        if (temporaryStock.produce_id == "") {
            temp_str += "Produce, "
        }
        if (temporaryStock.quantity_suffix_id == "") {
            temp_str += "Suffix, "
        }
        if (temporaryStock.variety_id == "") {
            temp_str += "Variety, "
        }
        if (temporaryStock.quantity == "") {
            temp_str += "Quantity, "
        }
        if (initial_len != temp_str.length) {
            //if missing fields, alert and return
            alert(temp_str.substring(0, temp_str.length - 2));
            return null;
        }

        //validate quantity inputs
        const parsed_quantity = parseInt(temporaryStock.quantity, 10);
        if (isNaN(parsed_quantity)) {
            console.log(parsed_quantity);
            alert("Invalid quantity input.");
            return null;
        } else {
            postObject['quantity'] = parsed_quantity;
        }

        if (temporaryStock.quantity_available != null && temporaryStock.quantity_available != "") {
            const parsed_quantity_available = parseInt(temporaryStock.quantity_available, 10);
            if (isNaN(parsed_quantity_available)) {
                alert("Invalid quantity available input.");
                return null;
            } else {
                postObject['quantity_available'] = parsed_quantity_available;
            }
        }

        return postObject;
    }

    const handleStockCreateSubmit = (event) => {
        event.preventDefault();

        let ret = createStockObjectAndValidateInputs();
        if (ret == null) {
            return;
        }

        //send off the request
        axiosInstance.post(`stock/`, ret)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });

        clearTemporaryStock();

        setDisplayCreateModal(false);

        reloadStock();

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

    const [seededDateValue, setSeededDateValue] = useState(null);
    const handleSeededDateChange = (newValue) => {
        setSeededDateValue(dayjs(newValue).format('YYYY-MM-DD')); //set value for the date input field
        const newFormData = { ...temporaryStock };
        newFormData["date_seeded"] = dayjs(newValue).format('YYYY-MM-DD');
        setTemporaryStock({ ...newFormData });
    };

    const [plantedDateValue, setPlantedDateValue] = useState(null);
    const handlePlantedDateChange = (newValue) => {
        setPlantedDateValue(dayjs(newValue).format('YYYY-MM-DD')); //set value for the date input field
        const newFormData = { ...temporaryStock };
        newFormData["date_planted"] = dayjs(newValue).format('YYYY-MM-DD');
        setTemporaryStock({ ...newFormData });
    };

    const [pickedDateValue, setPickedDateValue] = useState(null);
    const handlePickedDateChange = (newValue) => {
        setPickedDateValue(dayjs(newValue).format('YYYY-MM-DD')); //set value for the date input field
        const newFormData = { ...temporaryStock };
        newFormData["date_picked"] = dayjs(newValue).format('YYYY-MM-DD');
        setTemporaryStock({ ...newFormData });
    };

    const [ehd, setEHD] = useState(null);
    const handleEHD = (newValue) => {
        setEHD(dayjs(newValue).format('YYYY-MM-DD').toString()); //set value for the date input field
        const newFormData = { ...temporaryStock };
        newFormData["ehd"] = dayjs(newValue).format('YYYY-MM-DD');
        setTemporaryStock({ ...newFormData });
    };


    const [displayDatesModel, setDisplayDatesModel] = useState(false);
    const [tempDates, setTempDates] = useState({
        date_picked: "",
        date_planted: "",
        date_seeded: "",
        ehd: "",
        date_completed: "",
    });
    function updateDates(row) {
        const newFormData = { ...tempDates };
        newFormData["date_picked"] = row.date_picked;
        newFormData["date_planted"] = row.date_planted;
        newFormData["date_seeded"] = row.date_seeded;
        newFormData["ehd"] = row.ehd;
        newFormData["date_completed"] = row.date_completed;
        setTempDates({ ...newFormData });
    }
    const handleDatesClick = (event, row) => {
        updateDates(row);

        setDisplayDatesModel(true);
    }

    const handleCompleteClick = (event, row) => {
        axiosInstance.get('stock/' + row.id + '/toggle_date_completed/')
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });
        reloadStock();
        sendNotification({ msg: 'Success: Stock Completed', variant: 'success' });
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
                            >Create Stock</Button>
                        </Grid>
                    </Grid>
                </Box>

                <TableContainer component={Paper} style={{}}>
                    <Table aria-label="simple table" style={{}}>
                        <colgroup>
                            <col style={{ width: '4%' }} />
                            <col style={{ width: '12%' }} />
                            <col style={{ width: '12%' }} />
                            <col style={{ width: '12%' }} />
                            <col style={{ width: '12%' }} />
                            <col style={{ width: '16%' }} />
                            <col style={{ width: '7%' }} />
                            <col style={{ width: '22%' }} />
                        </colgroup>
                        <TableHead>
                            <TableRow
                                sx={{
                                    "& th": {
                                        fontSize: "1.05rem",
                                    }
                                }}
                            >
                                <TableCell className="tableCell">ID</TableCell>
                                <TableCell className="tableCell">Produce</TableCell>
                                <TableCell className="tableCell">Variety</TableCell>
                                <TableCell className="tableCell">Suffix</TableCell>
                                <TableCell className="tableCell">Quantity</TableCell>
                                <TableCell className="tableCell">Quantity Available</TableCell>
                                <TableCell className="tableCell">Completed</TableCell>
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
                                    {row.date_completed == null &&
                                        <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                            <PendingActionsIcon />
                                        </TableCell>
                                    }
                                    {row.date_completed != null &&
                                        <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                            <CheckBoxIcon sx={{ color: "#028357" }} />
                                        </TableCell>
                                    }

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
                                            onClick={(event) => { handleEditClick(event, row); }}
                                        >Edit</Button>

                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#028357",
                                                borderColor: "#028357",
                                                width: "90px",
                                                margin: "10px",
                                            }}
                                            onClick={(event) => handleCompleteClick(event, row)}
                                        >Complete</Button>

                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#FF0000",
                                                borderColor: "#FF0000",
                                                margin: "10px",
                                                width: "90px",
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


            {/* Modal for CREATE Stock */}
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
                                onChange={handleQuantityChange}
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
                onClick={() => { setDisplayCreateModal(!displayCreateModal); clearTemporaryStock(); }}
            />




            <div className={`Modal Large ${displayEditModal ? "Show" : ""}`}>
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
                }}>Edit Stock</Typography>


                <Box component="form" onSubmit={handleEditSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <Box noValidate>
                        <FormControl sx={{ width: "200px", mt: 2 }} required>
                            <InputLabel id="demo-simple-select-label">Supplier</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
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
                                onChange={handleQuantityChange}
                                sx={{ width: "200px" }}
                                variant="filled"
                            />
                        </FormControl>
                        <FormControl sx={{ width: "200px" }}>
                            <TextField
                                margin="normal"
                                name="produce_qty_available"
                                label="Available Quantity"
                                type="produce_qty_available"
                                id="produce_qty_available"
                                autoComplete="produce_qty_available"
                                size="small"
                                value={temporaryStock.quantity_available}
                                onChange={handleQuantityAvailableChange}
                                sx={{ width: "200px", ml: 2 }}
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
                            Submit
                        </Button>
                    </Box>
                </Box>

            </div>

            <div
                className={`Overlay ${displayEditModal ? "Show" : ""}`}
                onClick={() => { setDisplayEditModal(!displayEditModal); clearTemporaryStock(); }}
            />




            <div className={`Modal Medium ${displayDatesModel ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayDatesModel(!displayDatesModel); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>Stock Dates</Typography>
                <Typography fontSize="18px" sx={{ mt: 2, textAlign: 'center' }}> Date Seeded: {tempDates.date_seeded} </Typography>
                <Typography fontSize="18px" sx={{ mt: 2, textAlign: 'center' }}> Date Planted: {tempDates.date_planted} </Typography>
                <Typography fontSize="18px" sx={{ mt: 2, textAlign: 'center' }}> Date Picked: {tempDates.date_picked} </Typography>
                <Typography fontSize="18px" sx={{ mt: 2, textAlign: 'center' }}> Earliest Harvest Date: {tempDates.ehd} </Typography>
                <Typography fontSize="18px" sx={{ mt: 2, textAlign: 'center' }}> Date Completed: {tempDates.date_completed} </Typography>

                <Box textAlign='center'>
                    <Button
                        type="normal"
                        variant="contained"
                        sx={{ mt: 1, mb: 2, textAlign: 'center' }}
                        onClick={() => setDisplayDatesModel(false)}
                    >
                        Close
                    </Button>
                </Box>

            </div>

            <div
                className={`Overlay ${displayDatesModel ? "Show" : ""}`}
                onClick={() => { setDisplayDatesModel(!displayDatesModel); clearTemporaryStock(); }}
            />

        </React.Fragment>
    )



}

export default StockTable;