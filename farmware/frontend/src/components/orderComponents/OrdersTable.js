import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';
import { ListItemText, Checkbox, MenuItem, Select, InputLabel, FormControl, TextField, Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import ordersData from "./mock-orders.json";
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import axiosInstance from '../../axios';

function OrdersTable() {
  const navigate = useNavigate();

  function handleViewOrderClick(order) {
    navigate("/view-order", { state: order });
  }

  const [temporaryOrder, setTemporaryOrder] = useState({
    id: -1,
    customer_id: -1,
    invoice_number: -1,
    order_date: "",
    completion_date: ""
  });

  const clearTemporaryOrderState = () => {
    const formValues = {
      id: -1,
      customer_id: -1,
      invoice_number: -1,
      order_date: "",
      completion_date: ""
    };
    setTemporaryOrder({ ...formValues });
  };

  const [displayCreateModal, setDisplayCreateModal] = useState(false);
  const [meState, setMeState] = useState([]);
  const [customersList, setCustomersList] = useState([]);

  const handleFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...temporaryOrder };
    newFormData[fieldName] = fieldValue;

    setTemporaryOrder({ ...newFormData });
  };

  const handleCustomerChange = (event) => {
    console.log('val:'+event.target.value)
    const newFormData = { ...temporaryOrder };
    newFormData["customer_id"] = event.target.value;
    setTemporaryOrder({ ...newFormData });
  };

  const handleCreateSubmit = (event) => {
    event.preventDefault();
    console.log("Submitted an order creation:")
    console.log(temporaryOrder)
    setDisplayCreateModal(false);
  };

  useEffect(() => {
    axiosInstance
      .get(`user/me/`, {
      })
      .then((res) => {
        setMeState(res.data);
        console.log(res.data);
      })
      .catch((err) => {
        alert("ERROR: user/me failed");
      });

      axiosInstance
      .get(`customer/`, {
      })
      .then((res) => {
        setCustomersList(res.data);
        console.log(res.data);
      })
      .catch((err) => {
        alert("ERROR: customer/ failed");
      });
  }, []);

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
                onClick={() => { setDisplayCreateModal(true); }}
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

      {/* Create Order Modal */}
      <div className={`Modal ${displayCreateModal ? "Show" : ""}`}>
        <button
          className="Close"
          onClick={() => { setDisplayCreateModal(!displayCreateModal);}}
        >
          X
        </button>

        <Typography variant="h4" sx={{
          fontFamily: 'Lato',
          fontWeight: 'bold',
          marginTop:"20px",
        }}>Create Order</Typography>

        <Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <TextField
              required
              margin="normal"
              id="invoice_number"
              label="Invoice Number"
              name="invoice_number"
              autoComplete="invoice_number"
              autoFocus
              size="small"
              onChange={handleFormChange}
              sx={{ width: "300px" }}
              variant="filled"
            />
            <TextField
              required
              margin="normal"
              name="order_date"
              label="Order Date"
              type="order_date"
              id="order_date"
              autoComplete="order_date"
              size="small"
              onChange={handleFormChange}
              sx={{ width: "300px"}}
              variant="filled"
            />
          <Box noValidate>
          <FormControl sx={{ width: "300px", mt: 1 }}>
            <InputLabel id="demo-simple-select-label">Customers</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={temporaryOrder.customer_id}
              label="Customer"
              onChange={handleCustomerChange}
            >
              {
                  customersList.map((customer) => {
                    return (
                      <MenuItem key={customer.id} value={customer.id}>
                        <ListItemText primary={customer.name} />
                      </MenuItem>
                    )
                  })
                }
            </Select>
          </FormControl>
          </Box>

          <Box noValidate>
            <Button
              type="submit"
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Create
            </Button>
          </Box>

        </Box>
      </div>

      {/* Below snippet makes it so that if you click out of the modal it exits. */}
      <div
        className={`Overlay ${displayCreateModal ? "Show" : ""}`}
        onClick={() => { setDisplayCreateModal(!displayCreateModal); }}
      />

    </>
  )
}

export default OrdersTable