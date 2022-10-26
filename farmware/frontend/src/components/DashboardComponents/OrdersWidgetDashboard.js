import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, Grid, Typography, Button, Box } from '@mui/material';
import CustomPieChart from "./CustomPieChart";

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

    const data = [
        { name: 'Group A', value: 400 },
        { name: 'Group B', value: 300 },
        { name: 'Group C', value: 300 },
        { name: 'Group D', value: 200 },
    ];

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

    const RADIAN = Math.PI / 180;
    const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);

        return (
            <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
                {`${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };

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
                                    textAlign: 'left',
                                }}
                            >
                                Open Orders
                            </Typography>
                            <Typography variant="p" color="#" component="h3" sx={{
                                textAlign: 'left',
                                mt: 1,
                            }}>
                                11
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
                                    textAlign: 'left',
                                }}
                            >
                                Available Stock
                            </Typography>
                            <Typography variant="p" color="#" component="h3" sx={{
                                textAlign: 'left',
                                mt: 1,
                            }}>
                                11
                            </Typography>

                            <Box textAlign='center'>
                                <Button variant="text" size="large" style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    mt: 1,
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
                                    textAlign: 'left',
                                }}
                            >
                                Customers
                            </Typography>
                            <Typography variant="p" color="#" component="h3" sx={{
                                textAlign: 'left',
                                mt: 1,
                            }}>
                                3
                            </Typography>

                            <Box textAlign='center'>
                                <Button variant="text" size="large" style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    mt: 1,
                                }} onClick={() => handleViewCustomersClick()}>
                                    View All Customers
                                </Button>
                            </Box>

                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            <CustomPieChart/>
        </>
    )
}

export default OrdersWidgetDashboard