# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
def dropColumns(dataBase):
    
    print("Dropping Columns")
    
    dataBase.drop(['<TICKVOL>'], axis = 1, inplace = True)
    dataBase.drop(['<VOL>'], axis = 1, inplace = True)
    dataBase.drop(['<SPREAD>'], axis = 1, inplace = True)
    dataBase.drop(['<DATE>'], axis = 1, inplace = True)
    dataBase.drop(['<TIME>'], axis = 1, inplace = True)
    
    return dataBase