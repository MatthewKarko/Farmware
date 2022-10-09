import React, { useState, useEffect, Fragment } from "react";
import { useLocation } from 'react-router-dom';
import '../../css/OrderTable.css';
import ordersData from "../DashboardComponents/mock-data-orders.json";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Button from '@mui/material/Button';

function OrderTable() {
  const location = useLocation();
  return (
    <>
      <div className="offset">
        <h1> {location.state.customer}</h1>

        <TableContainer component={Paper} className="table">
          <Table sx={{ maxWidth: 1000 }} aria-label="simple table">
            <TableHead sx={{ maxWidth: 1000 }} >
              <TableRow sx={{ maxWidth: 1000 }} >
                <TableCell className="tableCell">Item Name</TableCell>
                <TableCell className="tableCell">SUFFIX</TableCell>
                <TableCell className="tableCell">Quantity</TableCell>
                <TableCell className="tableCell"></TableCell>
              </TableRow>
            </TableHead>
            <TableBody sx={{ maxWidth: 1000 }} >
              {location.state.contents.map((row) => (
                <TableRow key={row.id} sx={{ maxWidth: 1000 }} >
                  <TableCell className="tableCell">{row.itemName}</TableCell>
                  <TableCell className="tableCell">{row.suffix}</TableCell>
                  <TableCell className="tableCell">{row.quantity}</TableCell>
                  <TableCell className="tableCell">
                    <Button variant="outlined" size="medium"
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

export default OrderTable