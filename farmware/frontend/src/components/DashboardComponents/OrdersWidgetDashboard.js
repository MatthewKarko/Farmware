import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';

import ordersData from "./mock-data-orders.json";
// import '../../css/DashboardWidgets.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

function OrdersWidgetDashboard() {

    const navigate = useNavigate();

    function handleClick(data) {
        navigate("/order",{state:data});
      }

    return (
        <>
            <Grid container spacing={5} alignItems="flex-end">
                {ordersData.map((data) => {
                    return (
                        <Grid item key={data.id} xs={12} md={4}>
                            <Card sx={{ border: 1, shadow: 5 }}>
                                <CardContent>
                                    <Typography
                                        gutterBottom
                                        variant="h6"
                                        component="h2"
                                        sx={{
                                            fontSize: '20px',
                                            textAlign: 'left',
                                            margin: "10px",
                                        }}
                                    >
                                        {data.customer}
                                    </Typography>
                                    <Typography variant="p" color="textSecondary" sx={{
                                        fontSize: '14px',
                                        textAlign: 'left',
                                        margin: "10px"
                                    }}>
                                        Date: {data.date}
                                    </Typography>

                                    
                                    {/* User order id to redirect to order page*/}
                                    <Button sx={{ margin: "10px" } } onClick={() => handleClick(data)}>
                                        View Order
                                    </Button>
                                </CardContent>
                            </Card>
                        </Grid>
                    );
                })}
            </Grid>
        </>
    )
}

export default OrdersWidgetDashboard