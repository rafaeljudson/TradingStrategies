# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 17:33:17 2020

@author: rafae
"""
import pandas as pd
import numpy as np


def netProfit (result):
    
    net_profit = 0
    
    for i in range(len(result)):
        
        net_profit = result["Result U$D"][i+1] + net_profit
    
    return round(net_profit)

def sharpeRatio (result):
    
    sharpe_ratio = result["Result U$D"].mean() / (result["Result U$D"].std())
    
    return round(sharpe_ratio, 2)

def kRatio (result):
    
    pass

    return

def maxDD (result):
    
    acum = 0
    maxDD = 0
    max_profit = 0
    
    for i in range(len(result)):
        
        acum = result["Result U$D"][i+1] + acum
        
        if acum > max_profit:
            
            max_profit = acum
            
        if (max_profit - acum) > maxDD:
            
            maxDD = max_profit - acum
            
    return round(maxDD)


def numberTrades (result):
    
    return len(result)

def winningTrades (result):
    
    count = 0 
    
    for i in range(len(result)):
        
        if result["Result U$D"][i+1] > 0 :
            
            count = count + 1
            
    return round((count / len(result)), 2)

def avgWinning (result) :
    
    avg = 0
    count = 0
    
    for i in range(len(result)):
        
        if result["Result U$D"][i+1] > 0 :
            
            avg   = result["Result U$D"][i+1] + avg
            count = count + 1
    
    return round((avg / count), 2)

def avgLosing (result) :
    
    avg = 0
    count = 0
    
    for i in range(len(result)):
        
        if result["Result U$D"][i+1] <= 0 :
            
            avg   = result["Result U$D"][i+1] + avg
            count = count + 1
    
    return round((avg / count), 2)

def performanceResults():
    
    performance = pd.DataFrame(columns = ['Market',
                                          'Net Profit',
                                          'Sharpe Ratio',
                                          'Max DD',
                                          '# of Trades',
                                          '% Win',
                                          'Avg. Win',
                                          'Avg. Loss'])
    
    return performance

def setperformanceResults(index, pair, result, performance):
    
    performance.loc[index, "Market"]   = pair
    performance["Net Profit"][index]   = netProfit(result)
    performance["Sharpe Ratio"][index] = sharpeRatio(result)
    performance["Max DD"][index]       = maxDD(result)
    performance["# of Trades"][index]  = numberTrades(result)
    performance["% Win"][index]        = winningTrades(result)
    performance["Avg. Win"][index]     = avgWinning(result)
    performance["Avg. Loss"][index]    = avgLosing(result)
    
    return performance