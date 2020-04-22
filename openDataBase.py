# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
import pandas as pd

def openDataBase(directory, pair):
    
    print("Opening the file: ", pair)
    
    path      = directory + pair + ".csv"
    dataBase  = pd.read_csv(path, sep = "\t")
    
    return dataBase