import React from "react";
import { Snackbar, Alert } from "@mui/material"

const SuccessAlert = (props) => {
    const { message } = props;
    const [open, setOpen] = React.useState(true);

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return; //so clicking something else doesn't close it.
        }
        setOpen(false);
    };

    return (
            <Snackbar open={open} autoHideDuration={4000} onClose={handleClose}>
                <Alert severity="success" sx={{ width: '100%',backgroundColor:"#028357",
                color:"#ffffff","& .MuiAlert-icon": {color: "#ffffff"} }}>
                    {message}
                </Alert>
            </Snackbar>
    )
};

export default SuccessAlert