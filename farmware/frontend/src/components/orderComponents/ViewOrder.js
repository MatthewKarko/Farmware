import React, { useState, useEffect, Fragment } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import { ListItemText, Checkbox, MenuItem, Select, InputLabel, FormControl, TextField, Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import orderItemsData from "./mock-order-items.json";
import axiosInstance from '../../axios';
import produceData from "./mock-produce.json";
import produceSuffixData from "./mock-produce-suffix.json";
import produceSuffixData2 from "./mock-produce-suffix-2.json";
import produceVarietyData from "./mock-produce-variety.json";
import produceVarietyData2 from "./mock-produce-variety-2.json";

function ViewOrder() {
    const navigate = useNavigate();
    const location = useLocation();

    const [customerName, setCustomerName] = useState("");

    function handleViewAssignedStock(order_item) {
        // alert("View stock clicked for produce id: " + order_item.produce_id);
        alert("This will show all the stock that has been added to the order with the produce id of the entry selected.")
        // navigate("/orders/view-order",{state:order});
    }

    function handleAddStock(order_item) {
        alert("This will show a list of stock with the produce id of the order item selected. From the stock list, the user can select a stock, input a quantity, and add it to the order. This is where the produce variety is chosen.")
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

    const [produceSelected, setProduceSelected] = useState("");
    const [produceQuantityInput, setProduceQuantityInput] = useState();

    const [produceSuffixes, setProduceSuffixes] = useState([]);
    const [suffixSelected, setSuffixSelected] = useState(-1);

    const handleProduceChange = (event) => {
        setProduceSelected(event.target.value);

        // Correct the displayed suffix and variety options, and clear any prior stored state.

        //remove all from the suffix state
        let len = produceSuffixes.length
        for (let i = 0; i < len; i++) {
            produceSuffixes.pop();
        }

        //Temporarily, it will switch between two suffix lists to demonstrate functionality
        if(len == 2){
            for (let i = 0; i < produceSuffixData2.length; i++) {
                produceSuffixes.push(produceSuffixData2[i]);
            }
        } else {
            for (let i = 0; i < produceSuffixData.length; i++) {
                produceSuffixes.push(produceSuffixData[i]);
            }
        }

        setSuffixSelected(-1);

        //now do same for varieties
        //remove all from the suffix state
        let len_var = produceVarieties.length
        for (let i = 0; i < len_var; i++) {
            produceVarieties.pop();
        }

        //Temporarily, it will switch between two varieties lists to demonstrate functionality
        if(len_var == 2){
            for (let i = 0; i < produceVarietyData2.length; i++) {
                produceVarieties.push(produceVarietyData2[i]);
            }
        } else {
            for (let i = 0; i < produceVarietyData.length; i++) {
                produceVarieties.push(produceVarietyData[i]);
            }
        }

        setVarietySelected(-1);
    };

    const handleSuffixChange = (event) => {
        setSuffixSelected(event.target.value);
    };

    const [produceVarieties, setProduceVarieties] = useState([]);
    const [varietySelected, setVarietySelected] = useState(-1);

    const handleVarietyChange = (event) => {
        setVarietySelected(event.target.value);
    };

    const handleFormChange = (event) => {
        event.preventDefault();
        if (!isNaN(+event.target.value)) {
            //is number
            setProduceQuantityInput(event.target.value)
        } else {
            alert("Invalid quantity input.");
        }
    };

    const [displayAddProduceModal, setDisplayAddProduceModal] = useState(false);

    const handleAddProduceSubmit = (event) => {
        event.preventDefault();

        //TO DO: CHECKS FOR VALID INPUT

        //ASSUMING VALID INPUT:
        alert("Submitted a produce add to order.\nProduce ID:" + produceSelected + "\nSuffix ID: " + suffixSelected + "\nVariety ID: " + varietySelected + "\nQuantity: " + produceQuantityInput)
        
        //CLEAR SELECTED FIELDS
        setProduceQuantityInput(0)
        setProduceSelected(-1)
        setVarietySelected(-1)
        setSuffixSelected(-1)
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
    if(produceSuffixes.length != 0){
        produceSuffixOptions = produceSuffixes.map((suf) => <MenuItem key={suf.id} value={suf.id}>
        <ListItemText primary={suf.suffix} />
   </MenuItem>);
    }

    //This is required to transfer the changes to produce variety list to the Select menu
    let produceVarietyOptions = null;
    if(produceVarieties.length != 0){
        produceVarietyOptions = produceVarieties.map((variety_val) => <MenuItem key={variety_val.id} value={variety_val.id}>
        <ListItemText primary={variety_val.variety} />
   </MenuItem>);
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
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Produce Name</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Variety</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>QTY SUFFIX</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Order QTY</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Stock QTY Added</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>View Assigned Stock</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Add Stock</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {orderItemsData.map((order_item) => (
                                <TableRow key={order_item.stock_id} >
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.produce_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.variety}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.SUFFIX}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.order_qty}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.stock_qty_added}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                        <Button variant="outlined" size="medium" onClick={() => handleViewAssignedStock(order_item)}
                                        >View Assigned Stock</Button>
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

            <div className={`Modal ${displayAddProduceModal ? "Show" : ""}`}>
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
                                label="Select a Suffix"
                                onChange={handleVarietyChange}
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
                        value={produceQuantityInput}
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



        </>
    )
}

export default ViewOrder