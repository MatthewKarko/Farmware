import React, { useCallback, useState } from "react";
import { PieChart, Pie, Cell } from "recharts";
import { Grid, Box, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import SquareIcon from '@mui/icons-material/Square';

const data = [
  { name: "Group A", value: 30 },
  { name: "Group B", value: 40 },
  { name: "Group C", value: 30 },
  { name: "Group D", value: 20 }
];

// Colors map to index in data
const COLORS = ["#01422d", "#028357", "#04b479", "#04cf8b"];

export default function CustomPieChart() {
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

        <Grid container>
        {/* Customer color square legend at the bottom indicating what each one is */}
        <List justify="center">
          {data.map( (entry,index) => {
            return (
              <ListItem key={index} disablePadding style={{justify:'center'}}>
                <ListItemIcon justify="center">
                  <SquareIcon sx={{ color: COLORS[index]}} justify="center"/>
                </ListItemIcon>
                <ListItemText primary={entry.name} justify="center"/>
              </ListItem>
            );
          })}
        </List>
        </Grid>
      </Box>
    </>
  );
}
