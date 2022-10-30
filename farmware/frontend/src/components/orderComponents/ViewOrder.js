import React, { useState, useEffect, Fragment } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import { ListItemText, Checkbox, MenuItem, Select, InputLabel, FormControl, TextField, Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import useNotification from "../alert/UseNotification";

function ViewOrder() {
    const navigate = useNavigate();
    const location = useLocation();
    const [msg, sendNotification] = useNotification(); //for the success alerts

    const [customerName, setCustomerName] = useState("");

    const [displayViewAssignedStock, setDisplayViewAssignedStock] = useState(false);
    const [displayAddStockModal, setDisplayAddStockModal] = useState(false);

    const [viewingOrderItemID, setViewingOrderItemID] = useState(-1);

    const [produceList, setProduceList] = useState([]);

    function handleViewAssignedStock(order_item) {
        //OPEN MODAL TO VIEW ASSIGNED STOCK. HERE THEY CAN BE DELETED.
        setViewingOrderItemID(order_item.id);
        //clear current
        setOrderItemStock([]);

        //make the request for orderItemsStockData
        axiosInstance
            .get('/order_item/' + order_item.id + '/get_assigned_stock/', {
            })
            .then((res) => {
                res.data.stock.map((data) => {
                    setOrderItemStock(orderItemStock => [...orderItemStock, data])
                })
            })
            .catch((err) => {
                alert("ERROR: GET /api/order_item/{id}/get_assigned_stock/ failed");
            });

        //clear temporary
        clearTemporaryStockAdded();
        
        setDisplayViewAssignedStock(true);
    }

    const [orderItemStock, setOrderItemStock] = useState([]);

    function handleAddStock(order_item) {
        setViewingOrderItemID(order_item.id);

        //clear current
        setOrderItemStock([]);

        //make the request for orderItemsStockData
        axiosInstance
            .get('/order_item/' + order_item.id + '/get_available_stock/', {
            })
            .then((res) => {
                res.data.stock.map((data) => {
                    setOrderItemStock(orderItemStock => [...orderItemStock, data])
                })
            })
            .catch((err) => {
                alert("ERROR: GET /api/order_item/{id}/get_available_stock/ failed.");
            });

        //clear temporary
        clearTemporaryStockAdded();

        setDisplayAddStockModal(true);
    }

    function markAsComplete() {
        //todays date
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        let todayDate = yyyy + '-' + mm + '-' + dd;

        //do a patch 
        var patchObject = {
            completion_date: todayDate
        }
        axiosInstance.patch('/order/' + location.state.id + "/", patchObject)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });

        navigate("/orders");
    }

    function addProduce() {
        // Bring up modal to add produce
        setDisplayAddProduceModal(true);
    }

    const [temporaryProduce, setTemporaryProduce] = useState({
        produce_id: "",
        quantity_suffix_id: "",
        produce_variety_id: "",
        quantity: "",
    });

    const [produceSuffixes, setProduceSuffixes] = useState([]);

    const clearTemporaryProduce = () => {
        const formValues = {
            produce_id: "",
            quantity_suffix_id: "",
            produce_variety_id: "",
            quantity: "",
        };
        setTemporaryProduce({ ...formValues });
    };

    const handleProduceChange = (event) => {
        //clear the temporary produce (since all the fields change)
        clearTemporaryProduce();

        //set new produce
        const newFormData = { ...temporaryProduce };
        newFormData["produce_id"] = event.target.value;
        newFormData["quantity_suffix_id"] = "";
        newFormData["produce_variety_id"] = "";
        newFormData["quantity"] = "";
        setTemporaryProduce({ ...newFormData });

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
        const newFormData = { ...temporaryProduce };
        newFormData["quantity_suffix_id"] = event.target.value;
        setTemporaryProduce({ ...newFormData });
    };

    const [produceVarieties, setProduceVarieties] = useState([]);

    const handleVarietyChange = (event) => {
        const newFormData = { ...temporaryProduce };
        newFormData["produce_variety_id"] = event.target.value;
        setTemporaryProduce({ ...newFormData });
    };

    const handleFormChange = (event) => {
        event.preventDefault();
        const newFormData = { ...temporaryProduce };
        newFormData["quantity"] = event.target.value;
        setTemporaryProduce({ ...newFormData });
    };

    const [displayAddProduceModal, setDisplayAddProduceModal] = useState(false);

    const handleAddProduceSubmit = (event) => {
        event.preventDefault();

        let postObject = createStockObjectAndValidateInputs();
        if (postObject == null) {
            return;
        }
        //send off the request
        axiosInstance.post(`order_item/`, postObject)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });

        clearTemporaryProduce();

        setDisplayAddProduceModal(false);

        reloadOrderItems();

        sendNotification({ msg: 'Success: Order Item Created', variant: 'success' });
    };

    function createStockObjectAndValidateInputs() {
        //send off the request
        var postObject = {
            order_id: location.state.id,
            produce_id: temporaryProduce.produce_id,
            quantity_suffix_id: temporaryProduce.quantity_suffix_id,
            produce_variety_id: temporaryProduce.produce_variety_id,
            // quantity: temporaryProduce.quantity,
            // quantity: 10
        }

        //TO DO: CHECKS FOR VALID INPUT
        if (temporaryProduce.produce_id < 0) {
            alert("ERROR: Please select a produce.");
            return null;
        }
        if (temporaryProduce.quantity_suffix_id < 0) {
            alert("ERROR: Please select a produce suffix.");
            return null;
        }
        if (temporaryProduce.produce_variety_id < 0) {
            alert("ERROR: Please select a produce variety.");
            return null;
        }

        //validate quantity inputs
        const parsed_quantity = parseInt(temporaryProduce.quantity, 10);
        if (isNaN(parsed_quantity)) {
            alert("Invalid quantity input.");
            return null;
        } else {
            postObject['quantity'] = parsed_quantity;
        }

        return postObject;
    }

    const [reloadFlag, setReloadFlag] = useState(false);
    const reloadOrderItems = () => {
        setOrderItems([]);
        setReloadFlag(!reloadFlag);
    }

    const [orderItems, setOrderItems] = useState([]);

    useEffect(() => {
        axiosInstance
            .get(`customer/` + location.state.customer_id + "/", {
            })
            .then((res) => {
                setCustomerName(res.data.name);
            })
            .catch((err) => {
                alert("ERROR: customer/{id}/ failed.");
            });

        axiosInstance
            .get('order/' + location.state.id + '/get_order_items/', {
            })
            .then((res) => {
                setOrderItems(res.data.order_items);
            })
            .catch((err) => {
                alert("ERROR: order items request failed");
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

    const [temporaryStockAdded, setTemporaryStockAdded] = useState([]);

    const handleRowQuantityChange = (event) => {
        event.preventDefault();

        //try parse int
        let quant_var = 0;
        if (event.target.value != "") { //if it's empty, just leave it as 0
            const parsed_quantity = parseInt(event.target.value, 10);
            if (isNaN(parsed_quantity)) {
                alert("Invalid quantity input. Must be a positive integer.");
                return null;
            }
            quant_var=parsed_quantity;
        }

        //parse the id to int
        const parsed_id = parseInt(event.target.id, 10);

        //find the id of quantity_suffix
        let qty_suf_id = -1;
        for (let i = 0; i < orderItemStock.length; i++) {
            if(orderItemStock[i].id == parsed_id){
                qty_suf_id = orderItemStock[i].quantity_suffix_id
                break;
            }
        }

        //check stock_id if already exists in data
        let len_var = temporaryStockAdded.length
        let found = false
        for (let i = 0; i < len_var; i++) {
            if (temporaryStockAdded[i].stock_id == parsed_id) {

                if (quant_var == 0) {
                    //remove it
                    temporaryStockAdded.splice(i, 1);
                } else {
                    temporaryStockAdded[i].quantity = quant_var;
                }
                found = true;
                break;
            }
        }
        if (!found) {
            const newFormData = {};
            newFormData["stock_id"] = parsed_id;
            newFormData["quantity"] = quant_var;
            newFormData["quantity_suffix_id"] = qty_suf_id;
            temporaryStockAdded.push(newFormData);
        }
    }

    const clearTemporaryStockAdded = () => {
        let len_var = temporaryStockAdded.length
        for (let i = 0; i < len_var; i++) {
            temporaryStockAdded.pop();
        }
    };

    const addStockToOrderItemSubmit = () => {
        // //check all the quantity are valid
        let found = false
        for (let i = 0; i < temporaryStockAdded.length; i++) {
            if (!isNaN(+temporaryStockAdded[i].quantity)) {
                //number
                if (temporaryStockAdded[i].quantity < 0) {
                    //error
                    alert("ERROR: Quantity must be greater than 0.");
                    return;
                }
            } else {
                //error
                alert("ERROR: Quantity must numeric.");
                return;
            }
        }

        var postObject = {
            items: temporaryStockAdded
        }

        //make call to add all the stock:
        axiosInstance.post('order_item/' + viewingOrderItemID + '/bulk_add_stock/', postObject)
            .catch((err) => {
                alert("Error code: " + err.response.status + "\n" + err.response.data.error);
            });

        reloadOrderItems();

        setDisplayAddStockModal(false);

        sendNotification({ msg: 'Success: Stock Added To Order', variant: 'success' });
    }


    const handleOrderItemDeleteClick = (event, row) => {
        event.preventDefault();
        axiosInstance
            .delete('order_item/' + row.id + '/', {
            })
            .catch((err) => {
                alert("ERROR: Failed to delete stock");
            });
        reloadOrderItems();
        sendNotification({ msg: 'Success: Order Item Deleted', variant: 'success' });
    };

    const handleOrderItemStockDelete = (stock_link_id) => {
        axiosInstance
            .delete('order_item_stock_link/' + stock_link_id + '/', {
            })
            .catch((err) => {
                alert("ERROR: Failed to delete stock link id");
            });

        setDisplayViewAssignedStock(false);

        reloadOrderItems();
        
        sendNotification({ msg: 'Success: Deleted Stock From Order', variant: 'success' });
    };

    return (
        <>
            <div className="main-content">
                <Box sx={{ width: '100%', height: '10%' }}>
                    <Grid container rowSpacing={0} columnSpacing={{ xs: 6, sm: 2, md: 4 }}
                        style={{ minHeight: '10vh' }}>

                        <Grid item xs={6}>
                            <Typography variant="h4" sx={{
                                fontFamily: 'Lato',
                                fontWeight: 'bold',
                            }}>{customerName}'s Order</Typography>

                            <Typography variant="h7" sx={{
                                fontFamily: 'Lato',
                                fontStyle: 'italic',
                            }}>Invoice: #{location.state.invoice_number}</Typography>
                        </Grid>

                        <Grid item xs={6} sx={{ textAlign: "right" }}>
                            <Button type="submit" variant="outlined" size="large" style={{
                                marginRight: "30px"
                            }}
                                onClick={() => { addProduce() }}
                            >Add Produce To Order</Button>

                            <Button type="submit" variant="outlined" size="large" style={{
                                color: "#028357",
                                borderColor: "#028357",
                                marginRight: "10px"
                            }}
                                onClick={() => { markAsComplete() }}
                            >Mark Order As Complete</Button>
                        </Grid>
                    </Grid>
                </Box>

                <TableContainer component={Paper} className="table" style={{ margin: "auto" }}>
                    <Table aria-label="simple table" style={{ margin: "auto" }}>
                        {/* <colgroup>
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '15%' }} />
                        </colgroup> */}
                        <TableHead>
                            <TableRow>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>ID</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce</TableCell>
                                {/* <TableCell className="tableCell" sx={{ textAlign: "center" }}>Name</TableCell> */}
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Variety</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Suffix</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Order QTY</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Stock QTY Added</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {orderItems.map((order_item) => (
                                <TableRow key={order_item.stock_id}>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_name}</TableCell>
                                    {/* <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_id}</TableCell> */}
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.variety_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity_suffix_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity_used}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                        <Button variant="outlined" size="medium" onClick={() => { handleViewAssignedStock(order_item) }}
                                        >View Stock</Button>
                                        <Button variant="outlined" size="medium"
                                            sx={{ ml: 2 }}
                                            onClick={() => handleAddStock(order_item)}
                                        >Add Stock</Button>
                                        <Button variant="outlined" size="medium"
                                            sx={{
                                                borderColor: "#FF0000", color: "#FF0000", ':hover': {
                                                    bgcolor: "#fff0f0",
                                                    borderColor: "#FF0000"
                                                },
                                                ml: 2,
                                                width: "90px",
                                            }}
                                            onClick={(event) => handleOrderItemDeleteClick(event, order_item)}
                                        >Delete</Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>


            </div>

            <div className={`Modal Large ${displayAddProduceModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayAddProduceModal(false); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>Add Produce</Typography>

                {/* Contains a table for produce options and its suffix. Can select one, and input a quantity */}

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
                                value={temporaryProduce.produce_id}
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
                                value={temporaryProduce.quantity_suffix_id}
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
                                value={temporaryProduce.produce_variety_id}
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
                        value={temporaryProduce.quantity}
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
                            Add To Order
                        </Button>
                    </Box>
                </Box>

            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayAddProduceModal ? "Show" : ""}`}
                onClick={() => { setDisplayAddProduceModal(false); }}
            />

            <div className={`Modal Large ${displayViewAssignedStock ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayViewAssignedStock(false); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>View Assigned Stock</Typography>

                <Typography variant="h6" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 1,
                    mb: 1,
                    textAlign: 'center'
                }}>Order Item ID: {viewingOrderItemID}</Typography>

                {/* A selectable list that shows all the assigned stock. */}
                {/* Can select a stock and click 'delete selected' to delete it. */}

                {/* <Box sx={{ width: "800px", height:"319px", margin: "auto" }}>
                    <DataGrid
                        rows={rows}
                        columns={columns}
                        pageSize={4}
                        rowsPerPageOptions={[5]}
                        checkboxSelection
                        onSelectionModelChange={(ids) => onRowsSelectionHandler(ids)}                        
                    />
                </Box> */}
                <TableContainer component={Paper} className="table" style={{ margin: "auto", maxWidth: "80%", maxHeight: "66%" }}>
                    <Table aria-label="simple table" style={{ margin: "auto" }}>
                        {/* <colgroup>
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '15%' }} />
                        </colgroup> */}
                        <TableHead>
                            <TableRow>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>ID</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Supplier</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Variety</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Suffix</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>QTY Added to Order</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {orderItemStock.map((order_item) => (
                                <TableRow key={order_item.stock_id}>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.supplier_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_variety}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity_suffix}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                        <Button variant="outlined" size="medium" sx={{
                                            borderColor: "#FF0000", color: "#FF0000", ':hover': {
                                                bgcolor: "#fff0f0",
                                                borderColor: "#FF0000"
                                            },
                                        }}
                                            onClick={() => handleOrderItemStockDelete(order_item.id)}
                                        >Delete</Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>


                <Box textAlign='center' sx={{ mt: 2 }}>
                    <Button variant="outlined" size="large"
                        onClick={() => setDisplayViewAssignedStock(false)}
                    >Close</Button>
                </Box>


            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayViewAssignedStock ? "Show" : ""}`}
                onClick={() => { setDisplayViewAssignedStock(false); }}
            />


            {/* Add stock modal */}
            <div className={`Modal Large ${displayAddStockModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayAddStockModal(false); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>Add Stock to Order</Typography>

                <Typography variant="h6" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 1,
                    mb: 1,
                    textAlign: 'center'
                }}>Order Item ID: {viewingOrderItemID}</Typography>

                {/* A selectable list that shows all the assigned stock. */}
                {/* Can select a stock and click 'delete selected' to delete it. */}
                <TableContainer component={Paper} className="table" style={{ margin: "auto", maxWidth: "80%", maxHeight: "60%" }}>
                    <Table aria-label="simple table" style={{ margin: "auto" }}>
                        {/* <colgroup>
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '15%' }} />
                        </colgroup> */}
                        <TableHead>
                            <TableRow>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Stock ID</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Supplier</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Variety</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Suffix</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>QTY Available</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Add QTY to Order</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {orderItemStock.map((order_item) => (
                                <TableRow key={order_item.stock_id}>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.supplier_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.variety_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity_suffix_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity_available}</TableCell>

                                    <TableCell className="tableCell" sx={{ textAlign: "center", alignSelf: "center" }}>
                                        <TextField
                                            // required
                                            margin="normal"
                                            name="produce_qty_row"
                                            label="QTY"
                                            type="produce_qty_row"
                                            id={order_item.id}
                                            autoComplete="produce_qty_row"
                                            size="small"
                                            // value={temporaryProduce.quantity}
                                            onChange={handleRowQuantityChange}
                                            sx={{ width: "100px", height: "30px", mt: 0 }}
                                            variant="filled"
                                        />
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>


                <Box textAlign='center' sx={{ mt: 2 }}>
                    <Button type="submit" variant="outlined" size="large" style={{
                        color: "#028357",
                        borderColor: "#028357",
                    }}
                        onClick={() => addStockToOrderItemSubmit()}
                    >Submit</Button>
                </Box>


            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayAddStockModal ? "Show" : ""}`}
                onClick={() => { setDisplayAddStockModal(false); }}
            />

        </>
    )
}

export default ViewOrder