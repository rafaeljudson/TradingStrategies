# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
import pandas as pd
import dropColumns
import renameColumns
import addDate

def formatDataBase(dataBase, start_date, end_date, multiplier):
    
    print("Formating the new DataFrame")
    
    formated = dropColumns.dropColumns(renameColumns.renameColumns(addDate.addDate(dataBase)))
    
    formated["Open"]  = formated["Open"] * multiplier
    formated["High"]  = formated["High"] * multiplier
    formated["Low"]   = formated["Low"] * multiplier
    formated["Close"] = formated["Close"] * multiplier
    
    formated = formated[start_date : end_date]
    
    return formated