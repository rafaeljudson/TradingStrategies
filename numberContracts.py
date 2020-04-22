# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
def numberContracts(formated, multiplier, capital, period):
    
    print("Adding the 'Number of Contracts' Column")
    
    #formated["Number of Contracts"] = round(capital / (multiplier * formated["Close"].rolling(period).std()))
    formated["Number of Contracts"] = 1
    formated = formated.dropna(axis = 0)
    
    return formated