# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:03:02 2020

@author: Rafael Valle
"""
import pandas as pd
import matplotlib.pyplot as plt
import openDataBase
import addDate
import dropColumns
import formatDataBase
import numberContracts
import renameColumns
import tableResult
import savingResult
import showResult
import strategyBollinger
import perfomanceResults


#List of all currencies that we want to backtest the breakout strategy
assets = {'Currencies':["CADCHF", "CADJPY", "CHFJPY", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPUSD", "USDBRL", "USDCAD", "USDCHF", "USDJPY"],
          'Value PIP in USD':[10.15, 8.99, 8.99, 6.90, 10.15, 11.55, 8.99, 10.00, 6.90, 10.15, 8.99, 10.00, 1.94, 6.90, 10.15, 8.99],
          'Multiplier':[100000, 1000, 1000, 100000, 100000, 100000, 1000, 100000, 100000, 100000, 1000, 100000, 100000, 100000, 100000, 1000]}

asset = pd.DataFrame.from_dict(assets)

directory = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\5M\\Currencies\\"

save = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\BackTest\\Momentum\\"

performance = pd.DataFrame(columns = ['Market',
                                      'Net Profit',
                                      'Sharpe Ratio',
                                      'Max DD',
                                      '# of Trades',
                                      '% Win',
                                      'Avg. Win',
                                      'Avg. Loss'])

for b in range(len(asset)):
    
    data = openDataBase.openDataBase(directory, asset["Currencies"][b])
    
    start_date = "2019-02-01 00:00:00"
    end_date   = "2019-12-30 00:00:00"
    
    data_format = formatDataBase.formatDataBase(data, start_date, end_date, asset["Multiplier"][b])
    
    add_contract = numberContracts.numberContracts(data_format, asset["Value PIP in USD"][b], 10000, 100)
    
    strategy = strategyBollinger.strategyBollinger(add_contract, asset["Currencies"][b], 1000)
    
    results = showResult.showResult(strategy)
    
    savingResult.savingResult(results, asset["Currencies"][b], save)
    
    performance.loc[b, "Market"]       = asset["Currencies"][b]
    performance["Net Profit"][b]       = perfomanceResults.netProfit(strategy)
    performance["Sharpe Ratio"][b]     = perfomanceResults.sharpeRatio(strategy)
    performance["Max DD"][b]           = perfomanceResults.maxDD(strategy)
    performance["# of Trades"][b]      = perfomanceResults.numberTrades(strategy)
    performance["% Win"][b]            = perfomanceResults.winningTrades(strategy)
    performance["Avg. Win"][b]         = perfomanceResults.avgWinning(strategy)
    performance["Avg. Loss"][b]        = perfomanceResults.avgLosing(strategy)

adress_performance = save + "Resume_Result_All.txt"
performance.to_csv(adress_performance , index=False, sep = ';')