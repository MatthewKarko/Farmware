import React from 'react'
import { Drawer, IconButton, List, ListItemButton, ListItemIcon, ListItemText} from '@mui/material'
import { useState } from 'react'
import MenuIcon from '@mui/icons-material/Menu';
import { useValue } from '../context/GlobalContextProvider';


const DrawerComp = () => {
    const [openDrawer, setOpenDrawer] = useState(false);
    const {state:{currentUser, pages} , dispatch} = useValue();
  return (
    <React.Fragment>
            <Drawer open={openDrawer}
            onClose={()=>setOpenDrawer(false)}
            >
                <List>
                    {
                        pages.map((page)=>(
                            <ListItemButton onClick={()=> setOpenDrawer(false)} href={`/${page.toLowerCase()}`}>
                            <ListItemIcon>
                                <ListItemText>
                                    {page}
                                </ListItemText>
                            </ListItemIcon>
                        </ListItemButton>
                        ))
                    }
                   

                </List>
            </Drawer>
            <IconButton sx={{color:'white', marginLeft:'auto'}} onClick={()=>setOpenDrawer(!openDrawer)}>
                <MenuIcon />

            </IconButton>

    </React.Fragment>
  )
}

export default DrawerComp