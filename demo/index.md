# Demo Page

Hi this is _markdown_ and it **works**!

## Table of Contents
[TOC]

## Images

![](monalisa.png)

## Code Blocks

```cs
var plt = new ScottPlot.Plot(600, 400);
double[,] imageData = DataGen.SampleImageData();
plt.AddHeatmap(imageData);
plt.SaveFig("monalisa.png");
```

## Tables

Name       | Charge | pipette (mM) | bath (mM)      
-----------|--------|--------------|----------
K          | +1     | 145          | 2.8
Na         | +1     | 13           | 145
Mg         | +2     | 1            | 2
Ca         | +2     | 0            | 1
HEPES      | -1     | 5            | 5
Gluconate  | -1     | 145          | 0           
Cl         | -1     | 10           | 148.8

## Dynamic Content

Page generated at {{TIME}} on {{DATE}} 🚀