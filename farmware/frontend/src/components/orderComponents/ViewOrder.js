import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import ordersData from "./mock-orders.json";

function OrdersTable() {
  const navigate = useNavigate();

    // function handleViewOrderClick(order) {
    //     navigate("/orders/view-order",{state:order});
    //   }

  return (
    <>
        <div className="main-content">
                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    paddingBottom: '20px',
                }}>Customer Name</Typography>

        {/* <TableContainer component={Paper} className="table" style={{ maxWidth: 800, margin:"auto"}}>
          <Table aria-label="simple table" style={{ maxWidth: 800, margin:"auto"}}>
            <TableHead>
              <TableRow>
                <TableCell className="tableCell">Order ID</TableCell>
                <TableCell className="tableCell">Customer</TableCell>
                <TableCell className="tableCell">Invoice Number</TableCell>
                <TableCell className="tableCell">Date Created</TableCell>
                <TableCell className="tableCell">Status</TableCell>
                <TableCell className="tableCell"></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {ordersData.map((order) => (
                <TableRow key={order.order_id}>
                  <TableCell className="tableCell">{order.order_id}</TableCell>
                  <TableCell className="tableCell">{order.customer}</TableCell>
                  <TableCell className="tableCell">{order.invoice_number}</TableCell>
                  <TableCell className="tableCell">{order.date}</TableCell>
                  <TableCell className="tableCell">{order.status}</TableCell>
                  <TableCell className="tableCell">
                    <Button variant="outlined" size="medium" onClick={() => handleViewOrderClick(order)}
                    >View Order</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer> */}

      </div>
    </>
  )
}

export default OrdersTable