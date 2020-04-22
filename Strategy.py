# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:38:38 2020

@author: Rafael Valle

"""
import pandas as pd
import numpy as np

def enterBuy(index, pair, dataframe, result, i):
    
    result.loc[index, "Currency"]         = pair
    result["Order"][index]                = "Buy"
    result["Enter Date"][index]           = dataframe["Date"][i]
    result["Enter Price"][index]          = dataframe["Open"][i]
    
    return result

def enterSell(index, pair, dataframe, result, i):
    
    result.loc[index, "Currency"]         = pair
    result["Order"][index]                = "Sell"
    result["Enter Date"][index]           = dataframe["Date"][i]
    result["Enter Price"][index]          = dataframe["Open"][i]
    
    return result

def exitBuy(index, dataframe, result, i):
    
    result["End Date"][index]  = dataframe["Date"][i-1]
    result["End Price"][index] = dataframe["Low"][i-2]
    
    return result

def exitSell(index, dataframe, result, i):
    
    result["End Date"][index]  = dataframe["Date"][i-1]
    result["End Price"][index] = dataframe["High"][i-2]
    
    return result

def tableResult():
    
    result = pd.DataFrame(columns = ['Currency',
                                     'Order',
                                     'Enter Date',
                                     'End Date',
                                     'Enter Price',
                                     'End Price',
                                     'Result Pips'])
    
    return result

def strategyMomentum(pair, dataframe, period, period_ma, multiplier):
    
    print("Starting the backtest...")
    
    result = tableResult()
    
    dataframe["Volatility"]     = dataframe["Close"] - dataframe["Open"]
    dataframe["Frequency"]      = ((dataframe["Close"] - dataframe["Open"]) ** 2) ** 0.5
    dataframe["Frequency_Mean"] = dataframe["Frequency"].rolling(period).mean()
    dataframe["Frequency_Std"]  = dataframe["Frequency"].rolling(period).std()
    dataframe["Close_MA"]       = dataframe["Close"].rolling(period_ma).mean() 
    dataframe = dataframe.dropna(axis = 0)
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    
    for i in range(len(dataframe)):
        
        cond_buy1  = dataframe["Volatility"][i-1] > (dataframe["Frequency_Mean"][i-1] + (multiplier * dataframe["Frequency_Std"][i-1]))
        cond_buy2  = dataframe["Close_MA"][i-1] > dataframe["Close_MA"][i-2]
        cond_sell1 = dataframe["Volatility"][i-1] < (-1 * (dataframe["Frequency_Mean"][i-1] + (multiplier * dataframe["Frequency_Std"][i-1])))
        cond_sell2 = dataframe["Close_MA"][i-1] < dataframe["Close_MA"][i-2]
        
        cond_exit_buy1  = dataframe["Close_MA"][i-1] < dataframe["Close_MA"][i-2]
        cond_exit_sell1 = dataframe["Close_MA"][i-1] > dataframe["Close_MA"][i-2]
        
        
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy and cond_exit_buy1:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Low"][i-2]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell and cond_exit_sell1:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["High"][i-2]
                
                inTradeSell = False
                
                index = index + 1
                
        else:
            
            if cond_buy1 and cond_buy2:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeBuy = True
                
            if cond_sell1 and cond_sell2:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeSell = True
                
    result["Result Pips"] = np.where(result["Order"] == "Buy", (result["End Price"] - result["Enter Price"]), -1*(result["End Price"] - result["Enter Price"]))
    
    return result