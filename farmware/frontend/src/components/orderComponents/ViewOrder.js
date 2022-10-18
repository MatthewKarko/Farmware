import React, { useState, useEffect, Fragment } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import orderData from "./mock-order-items.json";

function OrdersTable() {
    const navigate = useNavigate();
    const location = useLocation();

    function handleViewProduceClick(order_item) {
        alert("View produce clicked: " + order_item.stock_id);
        // navigate("/orders/view-order",{state:order});
    }

    function markAsComplete() {
        alert("Mark order as complete. Order id: " + location.state.id);
        // navigate("/orders/view-order",{state:order});
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
                                paddingBottom: '20px',
                            }}>Customer ID: {location.state.customer_id}, Order ID: {location.state.id}</Typography>

                        </Grid>

                        <Grid item xs={6} sx={{ textAlign: "right" }}>
                            <Button type="submit" variant="outlined" size="large" style={{
                                color: "#028357",
                                borderColor: "#028357",
                                marginRight: "10px"
                            }}
                                onClick={() => { markAsComplete() }}
                            >Mark As Complete</Button>
                        </Grid>
                    </Grid>
                </Box>

                <TableContainer component={Paper} className="table" style={{ margin: "auto" }}>
                    <Table aria-label="simple table" style={{ margin: "auto" }}>
                        <colgroup>
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '17%' }} />
                            <col style={{ width: '15%' }} />
                        </colgroup>
                        <TableHead>
                            <TableRow>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Stock ID</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Item</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Quantity</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Suffix</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Supplier</TableCell>
                                <TableCell className="tableCell" sx={{ textAlign: "center" }}></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {orderData.map((order_item) => (
                                <TableRow key={order_item.stock_id} >
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.stock_id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.item_name}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.qty}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.SUFFIX}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order_item.supplier_id}</TableCell>
                                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                                        <Button variant="outlined" size="medium" onClick={() => handleViewProduceClick(order_item)}
                                        >View Produce</Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>


            </div>
        </>
    )
}

export default OrdersTable