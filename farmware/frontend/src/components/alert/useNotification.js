import { useSnackbar } from 'notistack';
// import IconButton from "@mui/material/IconButton";
// import CloseIcon from "@mui/material/SvgIcon/SvgIcon";
import React, {Fragment, useEffect, useState} from "react";

const useNotification = () => {
    const [conf, setConf] = useState({});
    const { enqueueSnackbar } = useSnackbar();
    const action = key => (
        <>
            <IconButton onClick={() => { closeSnackbar(key) }}  sx={{color:"#FFFFFF", backgroundColor:"#FFFFFF"}}>
                <CloseIcon sx={{color:"#FFFFFF", backgroundColor:"#FFFFFF"}}/>
            </IconButton>
            <button onClick={() => { closeSnackbar(snackbarId) }}>
      Dismiss
    </button>
        </>
        
    );
    useEffect(()=>{
        if(conf?.msg){
            let variant = 'info';
            if(conf.variant){
                variant = conf.variant;
            }
            enqueueSnackbar(conf.msg, {
                variant: variant,
                autoHideDuration: 4000,
                action
            });
        }
    },[conf]);
    return [conf, setConf];
};

export default useNotification;