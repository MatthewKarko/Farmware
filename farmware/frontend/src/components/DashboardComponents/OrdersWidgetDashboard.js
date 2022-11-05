import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, Grid, Typography, Button, Box } from '@mui/material';
import CustomPieChart from "./CustomPieChart";
import axiosInstance from '../../axios';

function OrdersWidgetDashboard() {

    const navigate = useNavigate();

    function handleViewOrdersClick(data) {
        navigate("/orders");
    }

    function handleViewStockClick(data) {
        navigate("/stock");
    }

    function handleViewCustomersClick(data) {
        navigate("/customers");
    }

    const [stockList, setStockList] = useState([]);
    const [customerList, setCustomerList] = useState([]);
    const [orderList, setOrderList] = useState([]);

    const [reloadFlag, setReloadFlag] = useState([]);

    useEffect(() => {
        axiosInstance
            .get(`customer/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setCustomerList(customerList => [...customerList, data])
                })
            })


        axiosInstance
            .get(`stock/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setStockList(stockList => [...stockList, data])
                })
            })


        axiosInstance
            .get(`order/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setOrderList(orderList => [...orderList, data])
                })
            })

    }, [reloadFlag]);

    return (
        <>
            <Grid container spacing={5} alignItems="flex-end" width="100%">
                <Grid item key="orders" lg={4} sx={{ mt: 3 }}>
                    <Card sx={{ border: 1, shadow: 5 }}>
                        <CardContent>
                            <Typography
                                gutterBottom
                                variant="h6"
                                component="h2"
                                sx={{
                                    fontSize: '20px',
                                    textAlign: 'center',
                                }}
                            >
                                Open Orders
                            </Typography>
                            <Typography variant="p" color="#" component="h2" sx={{
                                textAlign: 'center',
                                mt: 1,
                            }}>
                                {orderList.length}
                            </Typography>

                            <Box textAlign='center'>
                                <Button variant="text" size="large" style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    mt: 1,
                                }} onClick={() => handleViewOrdersClick()}>
                                    View All Orders
                                </Button>
                            </Box>

                        </CardContent>
                    </Card>
                </Grid>


                <Grid item key="stock" lg={4} sx={{ mt: 3 }}>
                    <Card sx={{ border: 1, shadow: 5 }}>
                        <CardContent>
                            <Typography
                                gutterBottom
                                variant="h6"
                                component="h2"
                                sx={{
                                    fontSize: '20px',
                                    textAlign: 'center',
                                }}
                            >
                                Available Stock
                            </Typography>
                            <Typography variant="p" color="#" component="h2" sx={{
                                textAlign: 'center',
                                mt: 1.5,
                            }}>
                                {stockList.length}
                            </Typography>

                            <Box textAlign='center'>
                                <Button variant="text" size="large" style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    mt: 1.5,
                                }} onClick={() => handleViewStockClick()}>
                                    View All Stock
                                </Button>
                            </Box>

                        </CardContent>
                    </Card>
                </Grid>

                <Grid item key="customers" lg={4} sx={{ mt: 3 }}>
                    <Card sx={{ border: 1, shadow: 5 }}>
                        <CardContent>
                            <Typography
                                gutterBottom
                                variant="h6"
                                component="h2"
                                sx={{
                                    fontSize: '20px',
                                    textAlign: 'center',
                                }}
                            >
                                Current Customers
                            </Typography>
                            <Typography variant="p" color="#" component="h2" sx={{
                                textAlign: 'center',
                                mt: 1.5,
                            }}>
                                {customerList.length}
                            </Typography>

                            <Box textAlign='center'>
                                <Button variant="text" size="large" style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    mt: 2,
                                }} onClick={() => handleViewCustomersClick()}>
                                    View All Customers
                                </Button>
                            </Box>

                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            <CustomPieChart />
        </>
    )
}

export default OrdersWidgetDashboard