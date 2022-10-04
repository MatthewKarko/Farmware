import React from 'react'
import { createContext, useContext, useReducer, useEffect } from 'react'
import reducer from './reducer';


const STORAGE_KEY = 'MY_DATA'
const storage = {
    currentUser:null,
    pages:["Login", "Signup"]
}

const initialState = JSON.parse(localStorage.getItem(STORAGE_KEY)) || storage;

const Context = createContext(initialState);

export const useValue = () =>{
    return useContext(Context)
}



const GlobalContextProvider = ({children}) => {
  
  // localStorage.removeItem(STORAGE_KEY)
  // const [state, dispatch] = useReducer(reducer,initialState);
  const [state, dispatch] = useReducer(reducer, initialState);
  // useEffect(() => {
  //   dispatch({type: 'UPDATE_USER', payload: JSON.parse(localStorage.getItem(STORAGE_KEY).getItem('currentUser'))});
  // }, []);
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
  }, [state])

  useEffect(() => {
    var storage = JSON.parse(localStorage.getItem(STORAGE_KEY));
    console.log(storage);
  })

  return (
   <Context.Provider value={{state, dispatch}}>
      {children}
    </Context.Provider>
  )
}

export default GlobalContextProvider