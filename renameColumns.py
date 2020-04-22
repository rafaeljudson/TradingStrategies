# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
def renameColumns(dataBase):
    
    print("Renaming Columns")
    
    dataBase = dataBase.rename(columns = {"<OPEN>" : "Open", 
                                          "<HIGH>" : "High", 
                                          "<LOW>" : "Low",
                                          "<CLOSE>" : "Close"})
    
    return dataBase