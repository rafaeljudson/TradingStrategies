# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:38:38 2020

@author: Rafael Valle

"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AR

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
    result = result.dropna(axis = 0)
    
    return result

def strategyBollinger(pair, dataframe, period_ma):
    
    print("Starting the backtest...")
    
    result = tableResult()
    
    dataframe["Close_MA"]       = dataframe["Close"].rolling(period_ma).mean()
    dataframe["Close_MA_Std"]   = dataframe["Close"].rolling(period_ma).std()
    dataframe["Upper+2"]          = dataframe["Close_MA"] + 2 * dataframe["Close_MA_Std"]
    dataframe["Lower-2"]          = dataframe["Close_MA"] - 2 * dataframe["Close_MA_Std"]
    dataframe["Upper+3"]          = dataframe["Close_MA"] + 3 * dataframe["Close_MA_Std"]
    dataframe["Lower-3"]          = dataframe["Close_MA"] - 3 * dataframe["Close_MA_Std"]
    dataframe = dataframe.dropna(axis = 0)
    
    inTradeBuy  =  False
    inTradeSell = False
    
    take_profit = 0
    stop_loss   = 0
    index       = 1
    
    for i in range(len(dataframe)):
        
        cond_buy1  = dataframe["Close"][i-1] < dataframe["Lower-2"][i-1]
        
        cond_sell1 = dataframe["Close"][i-1] > dataframe["Upper+2"][i-1]
        
        
        cond_exit_buy1  = dataframe["Close"][i-1] > take_profit
        cond_exit_buy2  = dataframe["Close"][i-1] < stop_loss
        cond_exit_buy   = cond_exit_buy1 or cond_exit_buy2
        
        cond_exit_sell1 = dataframe["Close"][i-1] < take_profit
        cond_exit_sell2 = dataframe["Close"][i-1] > stop_loss
        cond_exit_sell  = cond_exit_sell1 or cond_exit_sell2
        
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy and cond_exit_buy :
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                take_profit = 0
                stop_loss   = 0
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell and cond_exit_sell:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                take_profit = 0
                stop_loss   = 0
                
                inTradeSell = False
                
                index = index + 1
                
        else:
            
            if cond_buy1:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                take_profit = dataframe["Close_MA"][i-1]
                stop_loss   = dataframe["Lower-3"][i-1]
                
                inTradeBuy = True
                
            if cond_sell1:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                take_profit = dataframe["Close_MA"][i-1]
                stop_loss   = dataframe["Upper+3"][i-1]
                
                inTradeSell = True
                
    result["Result Pips"] = np.where(result["Order"] == "Buy", (result["End Price"] - result["Enter Price"]), -1*(result["End Price"] - result["Enter Price"]))
    result = result.dropna(axis = 0)
    
    return result

def strategyMomentumII(pair, dataframe, period, multiplier):
    
    print("Starting the backtest...")
    
    result = tableResult()
    
    dataframe["Volatility"]     = dataframe["Close"] - dataframe["Open"]
    dataframe["Frequency"]      = ((dataframe["Close"] - dataframe["Open"]) ** 2) ** 0.5
    dataframe["Frequency_Mean"] = dataframe["Frequency"].rolling(period).mean()
    dataframe["Frequency_Std"]  = dataframe["Frequency"].rolling(period).std() 
    dataframe = dataframe.dropna(axis = 0)
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    
    for i in range(len(dataframe)):
        
        cond_buy  = dataframe["Volatility"][i-1] > (dataframe["Frequency_Mean"][i-1] + (multiplier * dataframe["Frequency_Std"][i-1]))
        cond_sell = dataframe["Volatility"][i-1] < (-1 * (dataframe["Frequency_Mean"][i-1] + (multiplier * dataframe["Frequency_Std"][i-1])))
                
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                inTradeSell = False
                
                index = index + 1
                
        else:
            
            if cond_buy:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeBuy = True
                
            if cond_sell:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeSell = True
                
    result["Result Pips"] = np.where(result["Order"] == "Buy", (result["End Price"] - result["Enter Price"]), -1*(result["End Price"] - result["Enter Price"]))
    result = result.dropna(axis = 0)
    
    return result

def strategyScalping(pair, dataframe, threshold):
    
    print("Starting the backtest...")
    
    result = tableResult()
    
    dataframe["Volatility"] = dataframe["Close"] - dataframe["Open"] 
    dataframe = dataframe.dropna(axis = 0)
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    
    for i in range(len(dataframe)):
        
        cond_buy1   = dataframe["Volatility"][i-1] > 0
        cond_buy2   = dataframe["Volume"][i-1] > threshold
        cond_sell1  = dataframe["Volatility"][i-1] < 0
        cond_sell2  = dataframe["Volume"][i-1] > threshold
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
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
    result = result.dropna(axis = 0)
    
    return result

def strategyPivot(pair, dataframe, threshold):
    
    print("Starting the backtest...")
    
    result = tableResult()
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    
    for i in range(len(dataframe)):
        
        cond_buy1   = dataframe["Close"][i-1] > dataframe["High"][i-3]
        cond_buy2   = dataframe["Close"][i-2] < dataframe["Close"][i-3]
        cond_buy3   = dataframe["Volume"][i-1] > threshold 
        cond_buy4   = dataframe["Volume"][i-2] > threshold
        
        cond_sell1   = dataframe["Close"][i-1] < dataframe["Low"][i-3]
        cond_sell2   = dataframe["Close"][i-2] > dataframe["Close"][i-3]
        cond_sell3   = dataframe["Volume"][i-1] > threshold 
        cond_sell4   = dataframe["Volume"][i-2] > threshold
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                inTradeSell = False
                
                index = index + 1
                
        else:
            
            if cond_buy1 and cond_buy2 and cond_buy3 and cond_buy4:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeBuy = True
                
            if cond_sell1 and cond_sell2 and cond_sell3 and cond_sell4:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeSell = True
                
    result["Result Pips"] = np.where(result["Order"] == "Buy", (result["End Price"] - result["Enter Price"]), -1*(result["End Price"] - result["Enter Price"]))
    result = result.dropna(axis = 0)
    
    return result

def strategyPivotII(pair, dataframe, multiplier, period):
    
    print("Starting the backtest...")
    
    result = tableResult()
    
    dataframe["Volatility"]  = dataframe["Close"] - dataframe["Open"]
    dataframe["Volume_Mean"] = dataframe["Volume"].rolling(period).mean()
    dataframe["Volume_Std"]  = dataframe["Volume"].rolling(period).std()
    dataframe = dataframe.dropna(axis = 0)
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    
    for i in range(len(dataframe)):
        
        cond_buy2   = dataframe["Volatility"][i-1] > 0
        cond_buy3   = dataframe["Volume"][i-1] > dataframe["Volume_Mean"][i-1] + (multiplier * dataframe["Volume_Std"][i-1]) 
        cond_sell2  = dataframe["Volatility"][i-1] < 0
        cond_sell3  = dataframe["Volume"][i-1] > dataframe["Volume_Mean"][i-1] + (multiplier * dataframe["Volume_Std"][i-1])  
        
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy:
                
                result["End Date"][index]  = dataframe["Date"][i]
                result["End Price"][index] = dataframe["Close"][i]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                inTradeSell = False
                
                index = index + 1
                
        else:
            
            if cond_buy2 and cond_buy3 :
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeBuy = True
                
            if cond_sell2 and cond_sell3 :
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeSell = True
                
    result["Result Pips"] = np.where(result["Order"] == "Buy", (result["End Price"] - result["Enter Price"]), -1*(result["End Price"] - result["Enter Price"]))
    result = result.dropna(axis = 0)
    
    return result

def strategyVwap(pair, dataframe, period):
    
    print("Starting the backtest...")
    
    result = tableResult()
    
    dataframe["Price_Mid"]         = ((((dataframe["High"] + dataframe["Low"]) / 2) ** 2) ** 0.5)
    dataframe["Volume_Price"]      = dataframe["Volume"] * dataframe["Price_Mid"]
    dataframe["Volume_Price_Acum"] = dataframe["Volume_Price"].rolling(period).sum()
    dataframe["Volume_Acum"]       = dataframe["Volume"].rolling(period).sum()
    dataframe["VWAP"]              = round(dataframe["Volume_Price_Acum"] / dataframe["Volume_Acum"], 2)
    dataframe = dataframe.dropna(axis = 0)
    
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    
    for i in range(len(dataframe)):
        
        cond_buy1   = dataframe["Close"][i-2] > dataframe["VWAP"][i-2]
        cond_buy2   = dataframe["Close"][i-1] < dataframe["VWAP"][i-1]
        cond_buy3   = dataframe["VWAP"][i-1] > dataframe["VWAP"][i-2]
        
        cond_sell1   = dataframe["Close"][i-2] < dataframe["VWAP"][i-2]
        cond_sell2   = dataframe["Close"][i-1] > dataframe["VWAP"][i-1]
        cond_sell3   = dataframe["VWAP"][i-1] < dataframe["VWAP"][i-2]
        
        cond_exit_buy    = dataframe["VWAP"][i-1] < dataframe["VWAP"][i-2]
        cond_exit_sell   = dataframe["VWAP"][i-1] > dataframe["VWAP"][i-2]
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy and cond_exit_buy :
                
                result["End Date"][index]  = dataframe["Date"][i]
                result["End Price"][index] = dataframe["Close"][i]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell and cond_exit_sell :
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["Enter Price"][index] = dataframe["Close"][i]
                
                inTradeSell = False
                
                index = index + 1
                
        else:
            
            if cond_buy1 and cond_buy2 and cond_buy3 :
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeBuy = True
                
            if cond_sell1 and cond_sell2 and cond_sell3 :
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["End Price"][index]          = dataframe["Open"][i]
                
                inTradeSell = True
                
    result["Result Pips"] = result["End Price"] - result["Enter Price"]
    result = result.dropna(axis = 0)
    
    return result

def strategyPinbar(pair, dataframe, volume):
    
    print("Starting the backtest...")
    
    dataframe["Freq"] = dataframe["Close"] - dataframe["Open"]
    
    result = tableResult()    
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    stop_loss    = 0
    
    for i in range(len(dataframe)):
        
        cond_buy1    = dataframe["Freq"][i-2] < 0
        cond_buy2    = dataframe["Freq"][i-1] == 0
        cond_buy3    = dataframe["Volume"][i-1] > volume
        
        cond_sell1   = dataframe["Freq"][i-2] > 0
        cond_sell2   = dataframe["Freq"][i-1] == 0
        cond_sell3   = dataframe["Volume"][i-1] > volume
        
        cond_exit_buy  = dataframe["Low"][i] < stop_loss
        
        cond_exit_sell = dataframe["High"][i] > stop_loss
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell:
                
                result["End Date"][index]  = dataframe["Date"][i-1]
                result["End Price"][index] = dataframe["Close"][i-1]
                
                inTradeSell = False
               
                index = index + 1
                
        else:
            
            if cond_buy1 and cond_buy2 and cond_buy3:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeBuy = True
                
            if cond_sell1 and cond_sell2 and cond_sell3:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeSell = True
                
    result["Result Pips"] = np.where(result["Order"] == "Buy", (result["End Price"] - result["Enter Price"]), -1*(result["End Price"] - result["Enter Price"]))
    result = result.dropna(axis = 0)
    
    return result

def strategyTabajara(pair, dataframe, period_short, period_long, volume):
    
    print("Starting the backtest...")
    
    dataframe["MA_short"] = dataframe["Close"].rolling(period_short).mean()
    dataframe["MA_long"]  = dataframe["Close"].rolling(period_long).mean()
    dataframe = dataframe.dropna(axis = 0)
    
    result = tableResult()    
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    
    for i in range(len(dataframe)):
        
        cond_buy1    = dataframe["MA_short"][i-1] > dataframe["MA_short"][i-2]
        cond_buy2    = dataframe["MA_long"][i-1] > dataframe["MA_short"][i-2]
        cond_buy3    = dataframe["Close"][i-1] > dataframe["Close"][i-2]
        cond_buy4    = dataframe["Close"][i-2] < dataframe["MA_short"][i-2]
        cond_buy5    = dataframe["Close"][i-1] > dataframe["MA_short"][i-1]
        cond_buy6    = dataframe["Volume"][i-1] > volume
        
        cond_sell1   = dataframe["MA_short"][i-1] < dataframe["MA_short"][i-2]
        cond_sell2   = dataframe["MA_long"][i-1] < dataframe["MA_short"][i-2]
        cond_sell3   = dataframe["Close"][i-1] < dataframe["Close"][i-2]
        cond_sell4   = dataframe["Close"][i-2] > dataframe["MA_short"][i-2]
        cond_sell5   = dataframe["Close"][i-1] < dataframe["MA_short"][i-1]
        cond_sell6   = dataframe["Volume"][i-1] > volume
        
        cond_exit_buy  = dataframe["Close"][i-1] < dataframe["MA_short"][i-1]
        
        cond_exit_sell = dataframe["Close"][i-1] > dataframe["MA_short"][i-1]
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy and cond_exit_buy:
                
                result["End Date"][index]  = dataframe["Date"][i]
                result["End Price"][index] = dataframe["Open"][i]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell and cond_exit_sell:
                
                result["End Date"][index]  = dataframe["Date"][i]
                result["End Price"][index] = dataframe["Open"][i]
                
                inTradeSell = False
               
                index = index + 1
                
        else:
            
            if cond_buy1 and cond_buy2 and cond_buy3 and cond_buy4 and cond_buy5 and cond_buy6:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeBuy = True
                
            if cond_sell1 and cond_sell2 and cond_sell3 and cond_sell4 and cond_sell5 and cond_sell6:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = dataframe["Date"][i]
                result["Enter Price"][index]          = dataframe["Open"][i]
                
                inTradeSell = True
                
    result["Result Pips"] = np.where(result["Order"] == "Buy", (result["End Price"] - result["Enter Price"]), -1*(result["End Price"] - result["Enter Price"]))
    result = result.dropna(axis = 0)
    
    return result

def strategyAR(pair, dataframe, volume):
    
    print("Starting the backtest...")
    
    train = dataframe["Close"]["2016-02-23 09:00:00" : "2017-02-23 09:00:00"]
    data  = dataframe["2017-02-23 09:05:00" : "2017-05-23 09:00:00"]
    
    model    = AR(train).fit(maxlag = 10)
    n_params = model.k_ar
    const    = model.params[0]
    predict_price = 0
    
    result = tableResult()    
    
    inTradeBuy =  False
    inTradeSell = False
    
    index = 1
    
    for i in range(len(data)):
        
        predict_price = const + predict_price
        
        for j in range(n_params):
            
            predict_price = round((data["Close"][i-j] * model.params[j+1] + predict_price),2)
            
        print("--------------")
        print(predict_price)
        print(data["Close"][i])
        print("--------------")
        
        cond_buy1    = predict_price - data["Close"][i] > 1
        cond_buy2    = data["Volume"][i] > volume
        
        cond_sell1   = predict_price - data["Close"][i] < -1
        cond_sell2   = data["Volume"][i] > volume
        
        cond_exit_buy  = predict_price < data["Close"][i] 
        cond_exit_sell = predict_price > data["Close"][i]
        
        if inTradeBuy or inTradeSell:
            
            if inTradeBuy and cond_exit_buy:
                
                result["End Date"][index]  = data["Date"][i]
                result["End Price"][index] = data["Open"][i]
                
                inTradeBuy = False
                
                index = index + 1
                
            if inTradeSell and cond_exit_sell:
                
                result["End Date"][index]  = data["Date"][i]
                result["End Price"][index] = data["Open"][i]
                
                inTradeSell = False
               
                index = index + 1
                
        else:
            
            if cond_buy1 and cond_buy2:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Buy"
                result["Enter Date"][index]           = data["Date"][i]
                result["Enter Price"][index]          = data["Close"][i]
                
                inTradeBuy = True
                
            if cond_sell1 and cond_sell2:
                
                result.loc[index, "Currency"]         = pair
                result["Order"][index]                = "Sell"
                result["Enter Date"][index]           = data["Date"][i]
                result["Enter Price"][index]          = data["Close"][i]
                
                inTradeSell = True
        
        predict_price = 0
        
    result["Result Pips"] = np.where(result["Order"] == "Buy", (result["End Price"] - result["Enter Price"]), -1*(result["End Price"] - result["Enter Price"]))
    result = result.dropna(axis = 0)
    
    return result