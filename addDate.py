# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
import pandas as pd

def addDate(dataBase):
    
    print("Adding the 'Date' Column")
    
    dataBase["Index"] = dataBase['<DATE>'] + " " + dataBase['<TIME>']
    dataBase["Index"] = pd.to_datetime(dataBase["Index"], infer_datetime_format = True)
    dataBase["Date"] = dataBase["Index"]
    dataBase = dataBase.set_index("Index")
    
    return dataBase