import React, { useState, useEffect, Fragment } from "react";
import { useNavigate } from 'react-router-dom';
import { ListItemText, Checkbox, MenuItem, Select, InputLabel, FormControl, TextField, Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import axiosInstance from '../../axios';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import useNotification from "../alert/UseNotification";

function OrdersTable() {
  const navigate = useNavigate();
  const [msg, sendNotification] = useNotification(); //for the success alerts

  const [reloadFlag, setReloadFlag] = useState(false);
  const reloadOrders = () => {
    setOrdersList([]);
    setCustomersList([]);
    setReloadFlag(!reloadFlag);
  }

  const [temporaryOrder, setTemporaryOrder] = useState({
    customer_id: -1,
    invoice_number: "",
    order_date: "",
    completion_date: ""
  });

  const clearTemporaryOrderState = () => {
    setDateValue(null);
    const formValues = {
      customer_id: -1,
      invoice_number: "",
      order_date: "",
      completion_date: ""
    };
    setTemporaryOrder({ ...formValues });
  };

  const [displayCreateModal, setDisplayCreateModal] = useState(false);
  const [displayEditModal, setDisplayEditModal] = useState(false);

  const [customersList, setCustomersList] = useState([]);
  const [ordersList, setOrdersList] = useState([]);

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
    setDateValue(dayjs(newValue).format('YYYY-MM-DD'));
    const newFormData = { ...temporaryOrder };
    newFormData["order_date"] = dayjs(newValue).format('YYYY-MM-DD'); //set value for temporaryOrder
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

    //DO INPUT CHECKS:
    //Invoice number is a string < 20 characters, but can be empty
    if (temporaryOrder.invoice_number.length > 20) {
      //INVALID
      alert("ERROR: Invalid invoice number. Must be less than 20 characters");
      return;
    }

    //CHECK CUSTOMER ID IS NUMBER AND >= 0
    if (!isNaN(+temporaryOrder.customer_id)) {
      //Is number
      if (temporaryOrder.customer_id < 0) {
        //error
        alert("ERROR: Select a customer.");
        return;
      }
    } else {
      //not number: error
      alert("ERROR: Select a customer.");
      return;
    }

    if (temporaryOrder.order_date.length != 10) {
      //ERROR: not date format
      alert("ERROR: Invalid date format. Use DD/MM/YYYY." + temporaryOrder.order_date);
      return;
    }

    let temp_str = "Error! The following fields are required:\n"
    let initial_len = temp_str.length;

    if (temporaryOrder.customer_id == "") {
      temp_str += "Supplier, "
    }
    if (temporaryOrder.order_date == "") {
      temp_str += "Area Code, "
    }
    if (initial_len != temp_str.length) {
      //if missing fields, alert and return
      alert(temp_str.substring(0, temp_str.length - 2));
      return null;
    }

    //IF MADE IT HERE, IS VALID INPUT:
    var postObject = {
      order_date: temporaryOrder.order_date,
      customer_id: temporaryOrder.customer_id
    }
    if (temporaryOrder.completion_date != null && temporaryOrder.completion_date != "") {
      postObject['completion_date'] = temporaryOrder.completion_date;
    }
    if (temporaryOrder.invoice_number != null && temporaryOrder.invoice_number != "") {
      postObject['invoice_number'] = temporaryOrder.invoice_number;
    }

    axiosInstance.post(`order/`, postObject)
      .catch((err) => {
        alert("Error code: " + err.response.status + "\n" + err.response.data.error);
      });

    clearTemporaryOrderState();
    setDisplayCreateModal(false);

    //reload the data on page
    reloadOrders();
    sendNotification({ msg: 'Success: Order Created', variant: 'success' });
  };

  useEffect(() => {
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

    axiosInstance
      .get(`order/`, {
      })
      .then((res) => {
        setOrdersList(res.data);
        console.log(res.data);
      })
      .catch((err) => {
        alert("ERROR: order/ failed");
      });
  }, [reloadFlag]);

  const [edittingOrderID, setEdittingOrderID] = useState(-1);
  const handleEditClick = (event, row) => {
    event.preventDefault();

    setEdittingOrderID(row.id);

    //empty first
    clearTemporaryOrderState();

    if (row.order_date != null && row.order_date != "") {
      setDateValue(dayjs(row.order_date).format('YYYY-MM-DD'));
    }

    const formValues = {
      customer_id: row.customer_id,
      invoice_number: row.invoice_number,
      order_date: row.order_date,
      completion_date: row.completion_date
    };
    setTemporaryOrder({ ...formValues });

    setDisplayEditModal(true);
  }

  const handleDeleteClick = (event, row) => {
    event.preventDefault();
    axiosInstance
      .delete('order/' + row.id + '/', {
      })
      .catch((err) => {
        alert("ERROR: Failed to delete order");
      });
    reloadOrders();
    sendNotification({ msg: 'Success: Order Deleted', variant: 'success' });
  };

  const handleEditSubmit = (event) => {
    event.preventDefault();

    //VALIDATE INPUTS
    let ret = createOrderObjectAndValidateInputs();
    if (ret == null) {
        return; //alert already dislayed
    }

    //otherwise, send edit request
    axiosInstance.put('order/' + edittingOrderID + '/', ret)
        .catch((err) => {
            alert("Error code: " + err.response.status + "\n" + err.response.data.error);
        });

    setDisplayEditModal(false);

    clearTemporaryOrderState();

    reloadOrders();
    sendNotification({ msg: 'Success: Order Updated', variant: 'success' });
};

function createOrderObjectAndValidateInputs() {
  //send off the request
  var postObject = {
      customer_id: temporaryOrder.customer_id,
      order_date: temporaryOrder.order_date,
  }
  
  if (temporaryOrder.invoice_number != null && temporaryOrder.invoice_number != "") {
    if(temporaryOrder.invoice_number.length < 20){
      postObject['invoice_number'] = temporaryOrder.invoice_number;
    } else {
      alert("Error! Invoice number must be less than 20 characters long.");
      return;
    }
  }
  if (temporaryOrder.completion_date != null && temporaryOrder.completion_date != "") {
      postObject['completion_date'] = temporaryOrder.completion_date;
  }

  //CHECKS FOR INPUT
  let temp_str = "Error! The following fields are required:\n"
  let initial_len = temp_str.length;

  if (temporaryOrder.customer_id == "") {
      temp_str += "Customer, "
  }
  if (temporaryOrder.order_date == "" || temporaryOrder.order_date==null) {
      temp_str += "Order Date, "
  }
  if (initial_len != temp_str.length) {
      //if missing fields, alert and return
      alert(temp_str.substring(0, temp_str.length - 2));
      return null;
  }

  return postObject;
}

const handleCreateClick = () => {
  clearTemporaryOrderState();
  setDisplayCreateModal(true);
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
                onClick={() => { handleCreateClick(); }}
              >Create Order</Button>
            </Grid>
          </Grid>
        </Box>

        <TableContainer component={Paper} className="table" style={{ margin: "auto" }}>
          <Table aria-label="simple table" style={{ margin: "auto" }}>
            <colgroup>
              <col style={{ width: '4%' }} />
              <col style={{ width: '14%' }} />
              <col style={{ width: '14%' }} />
              <col style={{ width: '14%' }} />
              <col style={{ width: '14%' }} />
              <col style={{ width: '4%' }} />
              <col style={{ width: '25%' }} />
            </colgroup>
            <TableHead>
              <TableRow>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>ID</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Customer Name (is id atm)</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Invoice Number</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Date Created</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Completion Date</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}>Status</TableCell>
                <TableCell className="tableCell" sx={{ textAlign: "center" }}></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {ordersList.map((order) => (
                <TableRow key={order.order_id} >
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.id}</TableCell>
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.customer_id}</TableCell>
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.invoice_number}</TableCell>
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{dayjs(order.order_date).format('DD/MM/YYYY')}</TableCell>
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>{order.completion_date}</TableCell>
                  {order.completion_date == null &&
                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                      <PendingActionsIcon />
                    </TableCell>
                  }
                  {order.completion_date != null &&
                    <TableCell className="tableCell" sx={{ textAlign: "center" }}>
                      <CheckBoxIcon sx={{ color: "#028357" }} />
                    </TableCell>
                  }
                  <TableCell className="tableCell" sx={{ textAlign: "center" }}>

                    <Button variant="outlined" size="medium"
                      style={{
                        margin: "10px",
                        width: "90px",
                      }}
                      onClick={(event) => { handleEditClick(event, order); }}
                    >Edit</Button>

                    <Button variant="outlined" size="medium"
                      style={{
                        color: "#FF0000",
                        borderColor: "#FF0000",
                        margin: "10px",
                        width: "90px",
                      }}
                      onClick={(event) => handleDeleteClick(event, order)}
                    >Delete</Button>

                    <Button variant="outlined" size="medium"
                      style={{
                        margin: "10px",
                        width: "130px",
                      }}
                      onClick={() => handleViewOrderClick(event, order)}
                    >View Order</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>

      {/* Create Order Modal */}
      <div className={`Modal Large ${displayCreateModal ? "Show" : ""}`}>
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
          textAlign: "center"
        }}>Create Order</Typography>

        <Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <TextField
            margin="dense"
            id="invoice_number"
            label="Invoice Number"
            name="invoice_number"
            autoComplete="invoice_number"
            autoFocus
            size="small"
            value={temporaryOrder.invoice_number}
            onChange={handleFormChange}
            sx={{ width: "300px", mt: 3, mb: 3 }}
            variant="filled"
          />

          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DesktopDatePicker
              label="Date"
              name="order_date"
              inputFormat="DD/MM/YYYY"
              value={dateValue || null}
              // value={temporaryOrder.order_date}
              onChange={handleDateChange}
              renderInput={(params) => <TextField {...params} />}
              sx={{ width: "300px", mt: 3 }}
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


      <div className={`Modal Large ${displayEditModal ? "Show" : ""}`}>
        <button
          className="Close"
          onClick={() => { setDisplayEditModal(!displayEditModal); }}
        >
          X
        </button>

        <Typography variant="h4" sx={{
          fontFamily: 'Lato',
          fontWeight: 'bold',
          marginTop: "20px",
          textAlign: "center"
        }}>Edit Order</Typography>

        <Box component="form" onSubmit={handleEditSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <TextField
            margin="dense"
            id="invoice_number"
            label="Invoice Number"
            name="invoice_number"
            autoComplete="invoice_number"
            autoFocus
            size="small"
            value={temporaryOrder.invoice_number}
            onChange={handleFormChange}
            sx={{ width: "300px", mt: 3, mb: 3 }}
            variant="filled"
          />

          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DesktopDatePicker
              label="Date"
              name="order_date"
              inputFormat="DD/MM/YYYY"
              value={dateValue || null}
              // value={temporaryOrder.order_date}
              onChange={handleDateChange}
              renderInput={(params) => <TextField {...params} />}
              sx={{ width: "300px", mt: 3 }}
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
              Submit
            </Button>
          </Box>

        </Box>
      </div>

      {/* Below snippet makes it so that if you click out of the modal it exits. */}
      <div
        className={`Overlay ${displayEditModal ? "Show" : ""}`}
        onClick={() => { setDisplayEditModal(!displayEditModal); }}
      />

    </>
  )
}

export default OrdersTable