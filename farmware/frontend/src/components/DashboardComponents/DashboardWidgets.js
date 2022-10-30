import React, { useState, useEffect, Fragment } from "react";
import OrdersWidgetDashboard from './OrdersWidgetDashboard'
import '../../css/DashboardWidgets.css';
import Container from '@mui/material/Container';
import { Typography } from "@mui/material"

function DashboardWidgets() {
    return (
        <>
            <div>
                <Container maxWidth="md" component="main" sx={{ paddingTop: "0px", marginLeft: "0px" }}>
                    <Typography variant="h4" sx={{
                                fontFamily: 'Lato',
                                fontWeight: 'bold',
                            }}> Dashboard</Typography>
                    <OrdersWidgetDashboard />
                </Container>
            </div>
        </>
    )
}

export default DashboardWidgets