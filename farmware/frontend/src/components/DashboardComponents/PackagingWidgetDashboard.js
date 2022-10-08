import React, { useState, useEffect, Fragment } from "react";
import packagingData from "./mock-data-packaging.json";
import '../../css/DashboardWidgets.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import LinearProgress from '@mui/material/LinearProgress';

function PackagingWidgetDashboard() {
    return (
        <>
            <Grid container spacing={5} alignItems="flex-end">
                {packagingData.map((data) => {
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
                                        {data.packagingName}
                                    </Typography>
                                    <Typography variant="p" color="textSecondary" sx={{
                                        fontSize: '12px',
                                        textAlign: 'left',
                                        margin: "10px"
                                    }}>
                                        Quantity: {data.curQuantity}
                                    </Typography>
                                    <Typography variant="p" color="textSecondary" sx={{
                                        fontSize: '12px',
                                        textAlign: 'left',
                                        margin: "10px"
                                    }}>
                                        Max Quantity: {data.maxQuantity}
                                    </Typography>
                                    <LinearProgress sx={{ height: "15px", margin: "5px" }} variant="determinate" value={data.curQuantity} />

                                    <Button sx={{ margin: "5px" }}>
                                        See More Info
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

export default PackagingWidgetDashboard