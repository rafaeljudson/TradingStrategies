# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
import pandas as pd
import tableResult

def strategyBollinger(dataBase, pair, period):
    
    print("Initializing the BackTest")
    
    result = tableResult.tableResult()
    
    dataBase["Moving Average"]  = dataBase["Close"].rolling(period).mean()
    dataBase["Upper"] = dataBase["Moving Average"] + 2 * dataBase["Close"].rolling(period).std() 
    dataBase["Lower"]  = dataBase["Moving Average"] - 2 * dataBase["Close"].rolling(period).std()
    dataBase = dataBase.dropna(axis = 0)
    
    count              = 1 
    
    inTradeBuy  = False
    inTradeSell = False
    
    
    for i in range(len(dataBase)): 
        
        cond_to_enter_buy1 = dataBase["Close"][i] > dataBase["Upper"][i-1]
    
        cond_to_exit_buy1  = dataBase["Low"][i] < dataBase["Moving Average"][i-1]
        
        cond_to_enter_sell1 = dataBase["Close"][i] < dataBase["Lower"][i-1]
    
        cond_to_exit_sell1  = dataBase["High"][i] > dataBase["Moving Average"][i-1]
        
        if inTradeBuy or inTradeSell :    
           
            if inTradeBuy and cond_to_exit_buy1:
                
                result["End Date"][count]  = dataBase["Date"][i]
                result["End Price"][count] = round(dataBase["Moving Average"][i-1])
                result["Result"][count]    = round(1 * (result["End Price"][count] - result["Enter Price"][count]))
                result["Result U$D"][count]= round(result["Result"][count] * result["Numbers of Contracts"][count])
                
                inTradeBuy                 = False
                
                count                      = count + 1
            
            if inTradeSell and cond_to_exit_sell1 :
                
                result["End Date"][count]  = dataBase["Date"][i]
                result["End Price"][count] = round(dataBase["Moving Average"][i-1])
                result["Result"][count]    = round(-1 * (result["End Price"][count] - result["Enter Price"][count]))
                result["Result U$D"][count]= round(result["Result"][count] * result["Numbers of Contracts"][count])
                
                inTradeSell                = False
                
                count                      = count + 1
        
        else:
            
            if cond_to_enter_buy1:
                
                result.loc[count, "Currency"]         = pair
                result["Order"][count]                = "Buy"
                result["Enter Date"][count]           = dataBase["Date"][i]
                result["Enter Price"][count]          = round(dataBase["Open"][i])
                result["Numbers of Contracts"][count] = dataBase["Number of Contracts"][i-1]
                
                inTradeBuy                            = True
                
              
            if cond_to_enter_sell1: 
                
                result.loc[count, "Currency"]         = pair
                result["Order"][count]                = "Sell"
                result["Enter Date"][count]           = dataBase["Date"][i]
                result["Enter Price"][count]          = round(dataBase["Open"][i])
                result["Numbers of Contracts"][count] = dataBase["Number of Contracts"][i-1]
                
                inTradeSell                           = True
            
    
    
    
    return result