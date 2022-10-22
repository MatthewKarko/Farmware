import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';
import { ListItemText, Checkbox, MenuItem, Select, InputLabel, FormControl, TextField, Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import ordersData from "./mock-data/mock-orders.json";
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import axiosInstance from '../../axios';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';

function OrdersTable() {
  const navigate = useNavigate();

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
  const [custName, setCustName] = useState("");

  function handleViewOrderClick(order) {
    //get customer name based on id
    navigate("/view-order", { state: order });
  }

  const handleFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...temporaryOrder };
    newFormData[fieldName] = fieldValue;

    setTemporaryOrder({ ...newFormData });
  };

  // This state stores what is seen in the date selector, as it requires a different format to the temporaryOrder vlaue
  const [dateValue, setDateValue] = useState("");

  const handleDateChange = (newValue) => {
    setDateValue(newValue); //set value for the date input field
    const newFormData = { ...temporaryOrder };
    newFormData["order_date"] = dayjs(newValue).format('DD/MM/YYYY'); //set value for temporaryOrder
    setTemporaryOrder({ ...newFormData });
  };

  const handleCustomerChange = (event) => {
    console.log('val:' + event.target.value)
    const newFormData = { ...temporaryOrder };
    newFormData["customer_id"] = event.target.value;
    setTemporaryOrder({ ...newFormData });
  };

  const handleCreateSubmit = (event) => {
    event.preventDefault();
    alert("Submitted an order creation:\nOrder number: " + temporaryOrder.id + "\nInvoice number: " + temporaryOrder.invoice_number + "\ncustomer id: " + temporaryOrder.customer_id + "\nDate: " + temporaryOrder.order_date);
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
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Customer Name (is id atm)</TableCell>
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
          onClick={() => { setDisplayCreateModal(!displayCreateModal); }}
        >
          X
        </button>

        <Typography variant="h4" sx={{
          fontFamily: 'Lato',
          fontWeight: 'bold',
          marginTop: "20px",
          textAlign:"center"
        }}>Create Order</Typography>

        <Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <TextField
            required
            margin="dense"
            id="invoice_number"
            label="Invoice Number"
            name="invoice_number"
            autoComplete="invoice_number"
            autoFocus
            size="small"
            onChange={handleFormChange}
            sx={{ width: "300px", mt:3, mb:3 }}
            variant="filled"
          />

          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DesktopDatePicker
              label="Date"
              name="order_date"
              inputFormat="DD/MM/YYYY"
              value={dateValue}
              onChange={handleDateChange}
              renderInput={(params) => <TextField {...params} />}
              sx={{ width: "300px", mt:3 }}
            />
          </LocalizationProvider>

          <Box noValidate>
            <FormControl sx={{ width: "300px", mt: 3 }}>
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