import React, { useCallback, useState, useEffect, useMemo } from "react";
import { PieChart, Pie, Cell } from "recharts";
import { Grid, Box, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import SquareIcon from '@mui/icons-material/Square';
import axiosInstance from '../../axios';

// const data = [
//   { name: "New Open Orders", value: 0 },
//   { name: "Old Open Orders", value: 0 },
//   { name: "Completed Orders", value: 0 },
// ];

// Colors map to index in data
const COLORS = ["#01422d", "#028357", "#04b479", "#04cf8b"];

export default function CustomPieChart() {

  const [orderList, setOrderList] = useState([]);

  const [data, setData] = useState([]);

  useEffect(() => {
    axiosInstance
      .get(`order/`, {
      })
      .then((res) => {
        res.data.map((data) => {
          setOrderList(orderList => [...orderList, data])
        })
      })
  }, []);

  const getResult = useMemo(() => {
    // code that runs after the setting of the playerName and playerChoice. Will return "Win", "Lose", or "Draw"
    setupData()
}, [orderList]);

  function setupData() {

    let openNew = 0;
    let openOld = 0;
    let completed = 0;

    var today = new Date();

    for (let i = 0; i < orderList.length; i++) {
      if(orderList[i].completion_date != null){
        completed+=1;
      } else {
        //is open order. check if > 7 days old
        const orderDateVals = orderList[i].order_date.split("-");
        let date_of_order = new Date(orderDateVals[1] +"/" + orderDateVals[2] + "/"+orderDateVals[0]);
        let difference = today.getTime() - date_of_order.getTime();

        if (difference>604800000){ //greater than 7 days old
          openOld+=1;
        } else {
          openNew+=1;
        }
      }
    }

    if(orderList.length==0){
      let data_temp = [
        { name: "No Order Data", value: 1 },
      ];
      setData(data_temp);
      return;
    }

    let data_temp = [
      { name: "New Open Orders", value: openNew },
      { name: "Old Open Orders", value: openOld },
      { name: "Completed Orders", value: completed },
    ];

    setData(data_temp);
  }

  return (
    <>
      <Box width={400} height={450} border={1} mt={4} boxShadow={5}
        borderColor="#111111"
        textAlign="center"
        borderRadius={1}
      // display="flex"
      >
        <PieChart width={340} height={310} mt={0}>
          <Pie
            data={data}
            cx={195}
            cy={150}
            labelLine={false}
            // label={renderCustomizedLabel}
            label="aa"
            outerRadius={110}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
        </PieChart>

        {/* <Grid container> */}
        <Box
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          {/* <Box
        alignItems="left"
        width={200}
        height={100}> */}
          {/* Customer color square legend at the bottom indicating what each one is */}
          <List justify="center">
            {data.map((entry, index) => {
              return (
                <ListItem key={index} disablePadding style={{ justify: 'center' }}>
                  <ListItemIcon justify="center">
                    <SquareIcon sx={{ color: COLORS[index] }} justify="center" />
                  </ListItemIcon>
                  <ListItemText primary={entry.name} justify="center" />
                </ListItem>
              );
            })}
          </List>
          {/* </Grid> */}
          {/* </Box> */}
        </Box>
      </Box>
    </>
  );
}
