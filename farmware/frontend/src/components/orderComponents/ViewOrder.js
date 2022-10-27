import React, { useState, useEffect, Fragment } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import { ListItemText, Checkbox, MenuItem, Select, InputLabel, FormControl, TextField, Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import orderItemsData from "./mock-data/mock-order-items.json";
import axiosInstance from '../../axios';
import produceData from "./mock-data/mock-produce.json";
import produceSuffixData from "./mock-data/mock-produce-suffix.json";
import produceSuffixData2 from "./mock-data/mock-produce-suffix-2.json";
import produceVarietyData from "./mock-data/mock-produce-variety.json";
import produceVarietyData2 from "./mock-data/mock-produce-variety-2.json";
import orderItemsStockData from "./mock-data/mock-order-items-stock.json";

function ViewOrder() {
    const navigate = useNavigate();
    const location = useLocation();

    const [customerName, setCustomerName] = useState("");

    const [displayViewAssignedStock, setDisplayViewAssignedStock] = useState(false);
    const [displayAddStockModal, setDisplayAddStockModal] = useState(false);

    const [viewingOrderItemID, setViewingOrderItemID] = useState(-1);

    function handleViewAssignedStock(order_item) {
        //OPEN MODAL TO VIEW ASSIGNED STOCK. HERE THEY CAN BE DELETED OR MODIFIED.
        setViewingOrderItemID(order_item.id);
        //Using this order_item.id, can make a call to get all the order_items if necessary.
        setDisplayViewAssignedStock(true);
    }

    function handleAddStock(order_item) {
        setViewingOrderItemID(order_item.id);
        setDisplayAddStockModal(true);
        // alert("This will show a list of stock with the produce id of the order item selected. From the stock list, the user can select a stock, input a quantity, and add it to the order. This is where the produce variety is chosen.")
        // alert("Add stock clicked for produce_id: " + order_item.produce_id);
        // navigate("/orders/view-order",{state:order});
    }

    function markAsComplete() {
        alert("Mark order as complete. Order id: " + location.state.id);
        navigate("/orders");
    }

    function addProduce() {
        // Bring up modal to add produce
        setDisplayAddProduceModal(true);
    }

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

        //Temporarily, it will switch between two suffix lists to demonstrate functionality
        if (len == 2) {
            for (let i = 0; i < produceSuffixData2.length; i++) {
                produceSuffixes.push(produceSuffixData2[i]);
            }
        } else {
            for (let i = 0; i < produceSuffixData.length; i++) {
                produceSuffixes.push(produceSuffixData[i]);
            }
        }

        //now do same for varieties
        //remove all from the suffix state
        let len_var = produceVarieties.length
        for (let i = 0; i < len_var; i++) {
            produceVarieties.pop();
        }

        //Temporarily, it will switch between two varieties lists to demonstrate functionality
        if (len_var == 2) {
            for (let i = 0; i < produceVarietyData2.length; i++) {
                produceVarieties.push(produceVarietyData2[i]);
            }
        } else {
            for (let i = 0; i < produceVarietyData.length; i++) {
                produceVarieties.push(produceVarietyData[i]);
            }
        }
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

    useEffect(() => {
        axiosInstance
            .get(`customer/` + location.state.customer_id + "/", {
            })
            .then((res) => {
                setCustomerName(res.data.name);
                console.log(res.data.name);
            })
            .catch((err) => {
                alert("ERROR: customer/{id}/ failed. NOTE: THIS IS ONLY FAILING BECAUSE OF MOCK ORDER DATA.");
            });
    }, []);


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

        //check stock_id if already exists in data
        let len_var = temporaryStockAdded.length
        let found = false
        for (let i = 0; i < len_var; i++) {
            if (temporaryStockAdded[i].stock_id == event.target.id) {
                if (event.target.value == 0) {
                    //remove it
                    temporaryStockAdded.splice(i, 1);
                    console.log("its zero");
                } else {
                    temporaryStockAdded[i].quantity = event.target.value;
                }
                found = true;
                break;
            }
        }
        if (!found) {
            const newFormData = {};
            newFormData["stock_id"] = event.target.id;
            newFormData["quantity"] = event.target.value;
            temporaryStockAdded.push(newFormData);
        }
        console.log(temporaryStockAdded);
    }

    const clearTemporaryStockAdded = () => {
        let len_var = temporaryStockAdded.length
        for (let i = 0; i < len_var; i++) {
            temporaryStockAdded.pop();
        }
    };

    const addStockToOrderItemSubmit = () => {
        alert("send stock based on temporaryStockAdded array");
        clearTemporaryStockAdded();
        setDisplayAddStockModal(false);
    }

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
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce ID</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Name</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Variety</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>QTY SUFFIX</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Order QTY</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Stock QTY Added</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Assigned Stock</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Add Stock</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {orderItemsData.map((order_item) => (
                                <TableRow key={order_item.stock_id}>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.variety}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.SUFFIX}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.order_qty}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.stock_qty_added}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                        <Button variant="outlined" size="medium" onClick={() => { handleViewAssignedStock(order_item) }}
                                        >View Stock</Button>
                                    </TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                        <Button variant="outlined" size="medium" onClick={() => handleAddStock(order_item)}
                                        >Add Stock</Button>
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
                                value={temporaryProduce.produceSelected}
                            >
                                {
                                    produceData.map((produce) => {
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
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Stock ID</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Supplier</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce Name</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce Variety</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce SUFFIX</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>QTY Added to Order</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {orderItemsStockData.map((order_item) => (
                                <TableRow key={order_item.stock_id}>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.stock_id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.supplier_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_variety}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.suffix}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                        <Button variant="outlined" size="medium" sx={{
                                            borderColor: "#FF0000", color: "#FF0000", ':hover': {
                                                bgcolor: "#FFCCCB",
                                                borderColor:"#FF0000"
                                            },
                                        }}
                                        onClick={() => alert("delete stock_id: " + order_item.stock_id)}
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
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce Name</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce Variety</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce SUFFIX</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>QTY Available</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Add QTY to Order</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {orderItemsStockData.map((order_item) => (
                                <TableRow key={order_item.stock_id}>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.stock_id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.supplier_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_variety}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.suffix}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.quantity}</TableCell>

                                    <TableCell className="tableCell" sx={{ textAlign: "center", alignSelf: "center" }}>
                                        <TextField
                                            // required
                                            margin="normal"
                                            name="produce_qty_row"
                                            label="QTY"
                                            type="produce_qty_row"
                                            id={order_item.stock_id}
                                            autoComplete="produce_qty_row"
                                            size="small"
                                            // value={temporaryProduce.produceQuantity}
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