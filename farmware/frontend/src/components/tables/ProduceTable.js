import React, { useState, useEffect, Fragment } from "react";
import { Grid, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography, TextField } from "@mui/material"
import '../../css/PageMargin.css';
import '../../css/Modal.css';
import axiosInstance from '../../axios';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import { useNavigate } from "react-router-dom";

function ProduceTable() {

    const [produceList, setProduceList] = useState([]);
    const [displayEditModal, setDisplayEditModal] = useState(false);
    const [displayDeleteModal, setDisplayDeleteModal] = useState(false);
    const [displayCreateModal, setDisplayCreateModal] = useState(false);
    const [displaySuffixModal, setDisplaySuffixModal] = useState(false);
    const [displayVarietyModal, setDisplayVarietyModal] = useState(false);
    const [produceObj, setProduceObj] = useState([]);
    const [editProduceSuffix, setEditProduceSuffix] = useState([]);
    const [produceName, setProduceName] = useState("");
    const [currentProduceId, setCurrentProduceId] = useState(-1);
    const [produceSuffix, setProduceSuffix] = useState("");
    const [produceVarieties, setProduceVarieties] = useState([[]]);
    const [produceSuffixEquivalent, setProduceSuffixEquivalent] = useState();
    const [editModal, setEditModal] = useState(false);
    const [editRow, setEditRow] = useState();
    const [editView, setEditView] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        axiosInstance
            .get(`produce/`, {
            })
            .then((res) => {
                res.data.map((data) => {
                    setProduceList(produceList => [...produceList, data])
                    // console.log(res.data)
                })
            })
    }, []);

    const handleEditViewChange = (event) => {
        setEditView(event.target.value);
      };

    const handleEditView = (event) => {
        event.preventDefault();
        if(editView == 0){
            setDisplayEditModal(!displayEditModal);
        }else if (editView == 1){
            
            navigate('/edit-produce-suffix', {state: editRow});
        }else{
            navigate('/edit-produce-varieties', {state: editRow}); 
        }
        setEditModal(false);
      };

    const handleClickCloseEditModal = (event) => {
        event.preventDefault();
        setEditModal(false);
        setEditRow();
      };

    const handleClickOpenEditModal = (event, row) => {
        event.preventDefault();
        setEditModal(true);
        setEditRow(row);
      };

    const handleProduceNameChange = (event) => {
        event.preventDefault();
        setProduceName(event.target.value)
    };
    const handleProduceSuffixChange = (event) => {
        event.preventDefault();
        setProduceSuffix(event.target.value);
    };

    const handleVarietyChange = (event, i) => {
        event.preventDefault();
        const inputdata = [...produceVarieties];
        inputdata[i] = event.target.value;
        setProduceVarieties(inputdata);
        
    };
    const handleVarietyAdd = (event) => {
        event.preventDefault();
        setProduceVarieties(produceVarieties => [...produceVarieties, []]);
    };

    const handleVarietyDelete = (event, i) => {
        event.preventDefault();
        const deleteData = [...produceVarieties];
        deleteData.splice(i, 1);
        setProduceVarieties(deleteData);
    };

    

    const handleEditClick = (event, row) => {
        event.preventDefault();
        setDisplayEditModal(!displayEditModal);

        axiosInstance.get(`produce/${row.id}`)
            .then((res) => {
                console.log(res.data);
                setProduceObj(res.data);
                console.log(JSON.parse(res.data.quantity_suffixes));
                setEditProduceSuffix(JSON.parse(res.data.quantity_suffixes));
            })
    };

    const handleEditSubmit = (event) => {
        event.preventDefault();

    };

    const handleDeleteClick = (event, row) => {
        event.preventDefault();
        // setDisplayDeleteModal(!displayDeleteModal);


        axiosInstance.delete(`produce/${row.id}/`);
        // Confirmation modal
    };

    const handleDeleteSubmit = (event, row) => {
        event.preventDefault();
    };

    const handleCreateClick = () => {
        setDisplayCreateModal(!displayCreateModal);
    };

    const handleCreateSubmit = (event) => {
        event.preventDefault();
        
        var postObject = {
            name: produceName,
        };

        axiosInstance
            .post(`/produce/`, postObject)
            .then((res) => {
                setCurrentProduceId(res.data.id);
                setDisplayCreateModal(!displayCreateModal);
                setDisplaySuffixModal(!displaySuffixModal);
            })
            .catch((err)=> {
                console.log(err);
                alert(err.response.data.name);
                
                 });
        ;
        
        



    };

    const handleVarietySubmit = (event) => {
        event.preventDefault();
        var varietyResult = "[";
        varietyResult = varietyResult + produceVarieties.map(d => `"${d}"`).join(',');
        varietyResult = varietyResult + "]"
        console.log(varietyResult);
        // console.log(pr, currentProduceId);
        
        var postObject = {
            id: currentProduceId,
            name: varietyResult,

        };
        
        axiosInstance
                .post(`produce/${currentProduceId}/create_varieties/`, postObject)
                .catch((err) =>{console.log(err)})

        setDisplayVarietyModal(!displayVarietyModal);
        setProduceVarieties([[]]);

    }

    const handleProduceSuffixSubmit = (event) => {
        event.preventDefault();
        setDisplaySuffixModal(!displaySuffixModal);
        setDisplayVarietyModal(!displayVarietyModal);
        console.log(produceVarieties);
        var postObject = {
            produce_id: currentProduceId,
            suffix: produceSuffix,
            base_equivalent: produceSuffixEquivalent,
        };

        axiosInstance.post(`produce_quantity_suffix/`, postObject).then((res) => console.log(res.data)).catch((err)=> console.log(err));

        
    };
    const handleFormChange = (event) => {
        event.preventDefault();
        
        const fieldName = event.target.getAttribute("name");
        const fieldValue = event.target.value;
        
        const newFormData = { ...temporaryUser };
        newFormData[fieldName] = fieldValue;
        
        setProduceObj({ ...newFormData });
    };

    return (
        <React.Fragment>
            <div className="main-content">

                <Box sx={{ width: '100%', height: '10%' }}>
                    <Grid container rowSpacing={0} columnSpacing={{ xs: 6, sm: 2, md: 4 }}
                        style={{ minHeight: '10vh' }}>

                        <Grid item xs={6}>
                            <Typography variant="h4" sx={{
                                fontFamily: 'Lato',
                                fontWeight: 'bold',
                                paddingBottom: '20px',
                            }}>Produce Table</Typography>

                        </Grid>

                        <Grid item xs={6} sx={{ textAlign: "right" }}>
                            {/* <Box textAlign='center'> */}
                            <Button variant="outlined" size="large"
                                style={{
                                    color: "#028357",
                                    borderColor: "#028357",
                                    marginTop: "20px",
                                }}
                                onClick={(event) => handleCreateClick()}
                            >Create Produce</Button>
                        </Grid>
                    </Grid>
                </Box>

                <TableContainer component={Paper} >
                    <Table aria-label="simple table">
                        <colgroup>
                            <col style={{ width: '20%' }} />
                            <col style={{ width: '65%' }} />
                            <col style={{ width: '5%' }} />
                            <col style={{ width: '5%' }} />
                            <col style={{ width: '5%' }} />
                        </colgroup>
                        <TableHead>
                            <TableRow sx={{
                                "& th": {
                                    fontSize: "1.10rem",
                                }
                            }}>
                                <TableCell className="tableCell">Produce ID</TableCell>
                                <TableCell className="tableCell">Produce Name</TableCell>
                                <TableCell className="tableCell"></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {produceList.map((row) => (
                                <TableRow sx={{
                                    "& th": {
                                        fontSize: "1.10rem",
                                    }
                                }} key={row.id} >
                                    <TableCell className="tableCell">{row.id}</TableCell>
                                    <TableCell className="tableCell">{row.name}</TableCell>
                                    <TableCell className="tableCell">
                                        <Button variant="outlined" size="medium"
                                            style={{                                              
                                                width: "100px",
                                            }}
                                            onClick={(event) => handleClickOpenEditModal(event, row)}
                                        >Edit Produce</Button>
                                    </TableCell>
                                    <TableCell className="tableCell">
                                        <Button variant="outlined" size="medium"
                                            style={{
                                                color: "#FF0000",
                                                borderColor: "#FF0000",
                                                margin: "5px",
                                                width: "80px",
                                            }}
                                            onClick={(event) => handleDeleteClick(event, row)}
                                        >Delete</Button>
                                    </TableCell>

                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>

            </div>

            <Dialog open={editModal} onClose={handleClickCloseEditModal} >
                <DialogTitle>Select Option to Edit</DialogTitle>
                <DialogContent sx={{display: 'flex', flexDirection: 'column'}}>
                    <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">Options</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={editView}
                        label="Edit Option"
                        onChange={handleEditViewChange}
                        >
                        <MenuItem value={0}>Name</MenuItem>
                        <MenuItem value={1}>Quantity Suffix</MenuItem>
                        <MenuItem value={2}>Varieties</MenuItem>
                        </Select>
                    </FormControl>
                
                </DialogContent>
                <DialogActions>
                <Button onClick={handleClickCloseEditModal}>Cancel</Button>
                <Button onClick={handleEditView}>Edit</Button>
                </DialogActions>
            </Dialog>

            {/*Editing the produce */}
            <div className={`Modal ${displayEditModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayEditModal(!displayEditModal); clearState(); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    margin: "20px",
                    mt: 2,
                    textAlign: 'center'
                    }}> Edit Produce
                </Typography>


                <Box component="form" onSubmit={handleEditSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Box noValidate>
                        <TextField
                        InputLabelProps={{ shrink: !! produceObj.name }}
                        required
                        margin="normal"
                        id="name"
                        label="Produce Name"
                        name="name"
                        autoComplete="name"
                        autoFocus
                        size="small"
                        value={produceObj.name}
                        onChange={handleFormChange}
                        sx={{ width: "200px" }}
                        variant="filled"

                        />
                        <TextField

                        required
                        margin="dense"
                        name="last_name"
                        label="Lastname"
                        type="last_name"
                        id="last_name"
                        autoComplete="last_name"
                        size="small"
                        value={editProduceSuffix[0]?.suffix}
                        onChange={handleFormChange}
                        sx={{ width: "200px", mt: 2, ml: 2 }}
                        variant="filled"
                        />
                    </Box>
                </Box>

        
            </div>
            
            {/* Creating the Produce */}
            <div className={`Modal ${displayCreateModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayCreateModal(!displayCreateModal); setProduceName(""); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>Produce Name</Typography>
                <Box component="form" onSubmit={handleCreateSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <TextField
                        xs
                        required
                        margin="dense"
                        id="product_name"
                        label="Product Name"
                        name="produceName"
                        autoComplete="product_name"
                        autoFocus
                        size="small"
                        value={produceName}
                        onChange={handleProduceNameChange}
                        variant="filled"

                    />   

                    <Button
                        type="next"
                        variant="contained"
                        sx={{ mt: 3, mb: 2, bgcolor: 'blue' }}
                    >
                        Next
                    </Button>
                </Box>             
            </div>

            {/* Creating the Produce Suffix/Base Equivalent */}
            <div className={`Modal ${displaySuffixModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplaySuffixModal(!displaySuffixModal); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>Produce Suffix</Typography>
                <Box component="form" onSubmit={handleProduceSuffixSubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                    <TextField
                        xs
                        required
                        margin="dense"
                        id="produce_suffix"
                        label="Produce Suffix"
                        name="produceSuffix"
                        autoComplete="produce_suffix"
                        autoFocus
                        size="small"
                        value={produceSuffix}
                        onChange={handleProduceSuffixChange}
                        variant="filled"

                    /> 
                    <TextField
                        xs
                        required
                        InputProps={{ inputProps: { min: 1, max:100 } }}
                        margin="dense"
                        id="produce_suffix"
                        label="Suffix base equivalent"
                        name="produceSuffixEquivalent"
                        autoComplete="produceSuffixEquivalent"
                        autoFocus
                        size="medium"
                        type="number"
                        value={produceSuffixEquivalent}
                        onChange={(e) =>{setProduceSuffixEquivalent(parseInt(e.target.value))}}
                        variant="filled"
                        sx={{width: "150px"}}

                    />   

                    <Button
                        type="next"
                        variant="contained"
                        sx={{ mt: 3, mb: 2, bgcolor: 'blue' }}
                    >
                        Next
                    </Button>
                </Box>             
            </div>
            <div className={`Modal ${displayVarietyModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayVarietyModal(!displayVarietyModal); }}
                >
                    X
                </button>

                <Typography variant="h4" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    mt: 2,
                    textAlign: 'center'
                }}>Produce Varieties</Typography>
                <Box component="form" onSubmit={handleVarietySubmit} noValidate sx={{ mt: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    {produceVarieties.length < 4 && 
                    <Button
                        type="add"
                        variant="contained"
                        sx={{ mt: 1, mb: 2,  bgcolor: 'blue'}}
                        onClick={handleVarietyAdd}
                                    
                        >
                        Add
                    </Button> 
                    }     
                    {produceVarieties.map((variety, i) => {
                        return(
                          
                            <Box noValidate>                       
                                <TextField
                                xs
                                required
                                margin="dense"
                                id="produceVariety"
                                label="Produce Variety"
                                name="produceVariety"
                                autoComplete="produce_suffix"
                                autoFocus
                                size="small"
                                value={variety}
                                onChange={e=>handleVarietyChange(e,i)}
                                variant="filled"

                                />
                                


                                <Button
                                type="delete"
                                variant="contained"
                                sx={{ ml: 2, mt: 2, bgcolor: 'red' }}
                                onClick={e=>handleVarietyDelete(e,i)}
                                >
                                Delete
                                </Button>
                            </Box>
                          
                            
                        )

                    })}
                    <Button
                        type="create"
                        variant="contained"
                        sx={{ ml: 2, mt: 2, bgcolor: 'green' }}
                        >
                        Create Produce
                        </Button>
                </Box>             
            </div>

            <div className={`Modal ${displayDeleteModal ? "Show" : ""}`}>
                <button
                    className="Close"
                    onClick={() => { setDisplayDeleteModal(!displayEditModal); setProduceName(""); }}
                >X</button>

                <Typography variant="h5" sx={{
                    fontFamily: 'Lato',
                    fontWeight: 'bold',
                    margin: "20px",
                }}>Are you sure you want to delete the produce?</Typography>
                <Button type="submit" variant="outlined" size="large" style={{
                    color: "#FF0000",
                    borderColor: "#FF0000",
                }}
                    onClick={() => { setDisplayDeleteModal(!displayEditModal); handleDeleteSubmit(); }}
                >Delete</Button>
            </div>

            {/* Below snippet makes it so that if you click out of the modal it exits. */}
            <div
                className={`Overlay ${displayEditModal ? "Show" : ""}`}
                onClick={() => { setDisplayEditModal(!displayEditModal); }}
            />
            <div
                className={`Overlay ${displayDeleteModal ? "Show" : ""}`}
                onClick={() => { setDisplayDeleteModal(!displayDeleteModal); }}
            />
            <div
                className={`Overlay ${displayCreateModal ? "Show" : ""}`}
                onClick={() => { setDisplayCreateModal(!displayCreateModal); }}
            />
             <div
                className={`Overlay ${displaySuffixModal ? "Show" : ""}`}
                onClick={() => { setDisplaySuffixModal(!displaySuffixModal);}}
            />
            <div
                className={`Overlay ${displayVarietyModal ? "Show" : ""}`}
                onClick={() => { setDisplayVarietyModal(!displayVarietyModal);}}
            />
        </React.Fragment>
    )
}

export default ProduceTable