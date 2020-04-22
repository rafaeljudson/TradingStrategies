# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:50:25 2020

@author: Rafael Valle
"""
import pandas as pd
import matplotlib.pyplot as plt

def getDataFrame (adress, pair):
    
    print("Getting the price data")
    
    path = adress + pair + ".csv"
    dataframe = pd.read_csv(path, sep = '\t')
    
    return dataframe

def formatDataFrame (dataframe, decimal):
    
    print("Formating the price data to backtest")
    
    dataframe["Date"] = dataframe["<DATE>"] + " " + dataframe["<TIME>"]
    dataframe["Date"] = pd.to_datetime(dataframe["Date"], infer_datetime_format = True)
    dataframe = dataframe.set_index("Date", drop = False)
    
    dataframe = dataframe.rename(columns = {"<OPEN>" : "Open", 
                                            "<HIGH>" : "High", 
                                            "<LOW>" : "Low",
                                            "<CLOSE>" : "Close"})
    
    dataframe.drop(['<TICKVOL>'], axis = 1, inplace = True)
    dataframe.drop(['<VOL>'], axis = 1, inplace = True)
    dataframe.drop(['<SPREAD>'], axis = 1, inplace = True)
    dataframe.drop(['<DATE>'], axis = 1, inplace = True)
    dataframe.drop(['<TIME>'], axis = 1, inplace = True)
    
    dataframe["Open"]  = dataframe["Open"] * (10 ** decimal)
    dataframe["High"]  = dataframe["High"] * (10 ** decimal)
    dataframe["Low"]   = dataframe["Low"] * (10 ** decimal)
    dataframe["Close"] = dataframe["Close"] * (10 ** decimal)
    
    return dataframe

def savingResult(destination, pair, result):
    
    print("Saving the results of Backtest")
    
    path = destination + pair + ".txt"
    result.to_csv(path, index=False, sep = ';')
    
    return

def showingResult(result):
    
    plt.plot(result["End Date"], result["Result Pips"].cumsum())
    plt.grid(True)
    plt.xlabel('Date')
    plt.ylabel('Acum. Pips')
    plt.title('Result')
    return
    
def reportingResult(result):
    
    net_profit = 0
    
    for i in range(len(result)):
        
        net_profit = result["Result Pips"][i+1] + net_profit
        
    sharpe_ratio = result["Result Pips"].mean() / (result["Result Pips"].std())
    
    acum = 0
    maxDD = 0
    max_profit = 0
    
    for i in range(len(result)):
        
        acum = result["Result Pips"][i+1] + acum
        
        if acum > max_profit:
            
            max_profit = acum
            
        if (max_profit - acum) > maxDD:
            
            maxDD = max_profit - acum
            
    number_trades = len(result)
    
    win_trades = 0 
    
    for i in range(len(result)):
        
        if result["Result Pips"][i+1] > 0 :
            
            win_trades = win_trades + 1
            
    winning_trades = round(win_trades / len(result), 2)
            
    avg_w = 0
    count_w = 0
    
    for i in range(len(result)):
        
        if result["Result Pips"][i+1] > 0 :
            
            avg_w   = result["Result Pips"][i+1] + avg_w
            count_w = count_w + 1
            
    avg_winning_trades = round(avg_w / count_w, 2)
    
    avg_l = 0
    count_l = 0
    
    for i in range(len(result)):
        
        if result["Result Pips"][i+1] < 0 :
            
            avg_l   = result["Result Pips"][i+1] + avg_l
            count_l = count_l + 1
            
    avg_losing_trades = round(avg_l / count_l, 2)
    
    print("#################################################################")
    print("#################################################################")
    print("####                                                         ####")      
    print("####                     REPORTING RESULTS                   ####")     
    print("####                                                         ####")
    print("#################################################################")
    print("#################################################################") 
    print(" ")      
    print("Net Profit is: ", round(net_profit))
    print("Sharpe Ratio is: ", round(sharpe_ratio, 2))
    print("Max Drawdown is: ", round(maxDD, 2))
    print("Number of Trades is:  ", number_trades)
    print("Number of Winning trades is: ", win_trades)
    print("% of Winning trades is: ", winning_trades)
    print("Average Profit is: ", avg_winning_trades)
    print("Average Loss is: ", avg_losing_trades)
    
    return
    
def formatDataFrameVol (dataframe, decimal):
    
    print("Formating the price data to backtest")
    
    dataframe["Date"] = dataframe["<DATE>"] + " " + dataframe["<TIME>"]
    dataframe["Date"] = pd.to_datetime(dataframe["Date"], infer_datetime_format = True)
    dataframe = dataframe.set_index("Date", drop = False)
    
    dataframe = dataframe.rename(columns = {"<OPEN>" : "Open", 
                                            "<HIGH>" : "High", 
                                            "<LOW>" : "Low",
                                            "<CLOSE>" : "Close",
                                            "<VOL>" : "Volume"})
    
    dataframe.drop(['<TICKVOL>'], axis = 1, inplace = True)
    dataframe.drop(['<SPREAD>'], axis = 1, inplace = True)
    dataframe.drop(['<DATE>'], axis = 1, inplace = True)
    dataframe.drop(['<TIME>'], axis = 1, inplace = True)
    
    dataframe["Open"]  = dataframe["Open"] * (10 ** decimal)
    dataframe["High"]  = dataframe["High"] * (10 ** decimal)
    dataframe["Low"]   = dataframe["Low"] * (10 ** decimal)
    dataframe["Close"] = dataframe["Close"] * (10 ** decimal)
    
    return dataframe
