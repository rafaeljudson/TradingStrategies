# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
import pandas as pd
import tableResult

def strategyBreakout(dataBase, pair, period, multiplier):
    
    print("Initializing the BackTest")
    
    result = tableResult.tableResult()
    
    dataBase["Size of Candle"]  = (dataBase["Close"] - dataBase["Open"])
    dataBase["Volatility_Mean"] = (dataBase["Size of Candle"]).rolling(period).mean() 
    dataBase["Volatility_Std"]  = (dataBase["Size of Candle"]).rolling(period).std() 
    dataBase = dataBase.dropna(axis = 0)
    
    count       = 1
    
    inTradeBuy  = False
    inTradeSell = False
    
    for i in range(len(dataBase)): 
        
        if inTradeBuy or inTradeSell :    
           
            if inTradeBuy and (dataBase["Low"][i] < dataBase["Low"][i-1]):
                
                result["End Date"][count]  = dataBase["Date"][i]
                result["End Price"][count] = round(dataBase["Low"][i-1])
                result["Result"][count]    = round(1 * (result["End Price"][count] - result["Enter Price"][count]))
                result["Result U$D"][count]= round(result["Result"][count] * result["Numbers of Contracts"][count])
                
                inTradeBuy                 = False
                
                count                      = count + 1
            
            if inTradeSell and (dataBase["High"][i] > dataBase["High"][i-1]):
                
                result["End Date"][count]  = dataBase["Date"][i]
                result["End Price"][count] = round(dataBase["High"][i-1])
                result["Result"][count]    = round(-1 * (result["End Price"][count] - result["Enter Price"][count]))
                result["Result U$D"][count]= round(result["Result"][count] * result["Numbers of Contracts"][count])
                
                inTradeSell                = False
                
                count                      = count + 1
        
        else:
            
            if (dataBase["Size of Candle"][i-1] > (dataBase["Volatility_Mean"][i-1] + (multiplier * dataBase["Volatility_Std"][i-1]))):
                
                result.loc[count, "Currency"]         = pair
                result["Order"][count]                = "Buy"
                result["Enter Date"][count]           = dataBase["Date"][i]
                result["Enter Price"][count]          = round(dataBase["Open"][i])
                result["Numbers of Contracts"][count] = dataBase["Number of Contracts"][i-1]
                
                inTradeBuy                            = True
                
              
            if (dataBase["Size of Candle"][i-1] < -1 * (dataBase["Volatility_Mean"][i-1] + (multiplier * dataBase["Volatility_Std"][i-1]))): 
                
                result.loc[count, "Currency"]         = pair
                result["Order"][count]                = "Sell"
                result["Enter Date"][count]           = dataBase["Date"][i]
                result["Enter Price"][count]          = round(dataBase["Open"][i])
                result["Numbers of Contracts"][count] = dataBase["Number of Contracts"][i-1]
                
                inTradeSell                           = True
            
    
    
    
    return result