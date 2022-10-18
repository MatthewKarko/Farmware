import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import ordersData from "./mock-orders.json";
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import PendingActionsIcon from '@mui/icons-material/PendingActions';

function OrdersTable() {
  const navigate = useNavigate();

  function handleViewOrderClick(order) {
    navigate("/view-order", { state: order });
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
              }}>Orders Table</Typography>
            </Grid>

            <Grid item xs={6} sx={{ textAlign: "right" }}>
              <Button type="submit" variant="outlined" size="large" style={{
                color: "#028357",
                borderColor: "#028357",
                marginRight: "10px"
              }}
                onClick={() => { }}
              >Create Order</Button>
            </Grid>
          </Grid>
        </Box>

        <TableContainer component={Paper} className="table" style={{ margin: "auto" }}>
          <Table aria-label="simple table" style={{ margin: "auto" }}>
            <colgroup>
              <col style={{ width: '8%' }} />
              <col style={{ width: '12%' }} />
              <col style={{ width: '16%' }} />
              <col style={{ width: '20%' }} />
              <col style={{ width: '20%' }} />
              <col style={{ width: '10%' }} />
              <col style={{ width: '14%' }} />
            </colgroup>
            <TableHead>
              <TableRow>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Order ID</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Customer ID</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Invoice Number</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Date Created</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Completion Date</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Status</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {ordersData.map((order) => (
                <TableRow key={order.order_id} >
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.id}</TableCell>
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.customer_id}</TableCell>
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.invoice_number}</TableCell>
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.order_date}</TableCell>
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.completion_date}</TableCell>
                  {order.completion_date == "" &&
                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                      <PendingActionsIcon />
                    </TableCell>
                  }
                  {order.completion_date != "" &&
                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                      <CheckBoxIcon sx={{ color: "#028357" }} />
                    </TableCell>
                  }
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                    <Button variant="outlined" size="medium" onClick={() => handleViewOrderClick(order)}
                    >View Order</Button>
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