import React, { useState, useEffect, Fragment } from "react";
import PackagingWidgetDashboard from './PackagingWidgetDashboard.js'
import OrdersWidgetDashboard from './OrdersWidgetDashboard'
import '../../css/DashboardPages.css';
import Container from '@mui/material/Container';

function DashboardWidgets() {
    return (
        <>
            <div>
                <Container maxWidth="md" component="main" sx={{ paddingTop: "0px", marginLeft: "0px" }}>
                    <h2>Orders:</h2>
                    <OrdersWidgetDashboard />
                </Container>

                <Container maxWidth="md" component="main" sx={{ paddingTop: "50px", marginLeft: "0px" }}>
                    <h2>Packaging:</h2>
                    <PackagingWidgetDashboard />
                </Container>
            </div>
        </>
    )
}

export default DashboardWidgets