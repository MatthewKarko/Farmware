import { useSnackbar } from 'notistack';
import IconButton from "@mui/material/IconButton";
import React, {Fragment, useEffect, useState} from "react";

const useNotification = () => {
    const [conf, setConf] = useState({});
    const { enqueueSnackbar } = useSnackbar();
    useEffect(()=>{
        if(conf?.msg){
            let variant = 'info';
            if(conf.variant){
                variant = conf.variant;
            }
            enqueueSnackbar(conf.msg, {
                variant: variant,
                autoHideDuration: 4000,
            });
        }
    },[conf]);
    return [conf, setConf];
};

export default useNotification;