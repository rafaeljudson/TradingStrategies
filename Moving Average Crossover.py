# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:12:30 2020

@author: Rafael Valle

Description: Program created to clean and analize forex 5 minutes data using Moving Average Crossover strategy 
"""
#Importing libraries------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#List of all currencies that we want to backtest the moving average crossover strategy
assets = {'Currencies':["CADCHF", "CADJPY", "CHFJPY", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPUSD", "USDBRL", "USDCAD", "USDCHF", "USDJPY"],
          'Value PIP in USD':[10.15, 8.99, 8.99, 6.90, 10.15, 11.55, 8.99, 10.00, 6.90, 10.15, 8.99, 10.00, 1.94, 6.90, 10.15, 8.99]}

asset = pd.DataFrame.from_dict(assets)

#Reading all files
for a in range(len(asset)):
    #Reading the file---------------------------------------------------------------------
    path1 = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\5M\\Currencies\\"
    path2 = ".csv"
    path_final = path1+asset["Currencies"][a]+path2
    currency = pd.read_csv(path_final, sep = '\t')
    
    #Setting the period of backtest-------------------------------------------------------
    start_date = "2019-02-01 00:00:00"
    end_date   = "2019-12-30 00:00:00"
    
    #Formating the data and setting as index----------------------------------------------
    currency["Index"] = currency['<DATE>'] + " " + currency['<TIME>']
    currency["Index"] = pd.to_datetime(currency["Index"], infer_datetime_format = True)
    currency["Date"] = currency["Index"]
    currency = currency.set_index("Index")
    
    #Renaming the columns-----------------------------------------------------------------
    currency = currency.rename(columns = {"<OPEN>" : "Open", 
                                          "<HIGH>" : "High", 
                                          "<LOW>" : "Low",
                                          "<CLOSE>" : "Close"})
    
    #Droping the unnecessary columns------------------------------------------------------
    currency.drop(['<TICKVOL>'], axis = 1, inplace = True)
    currency.drop(['<VOL>'], axis = 1, inplace = True)
    currency.drop(['<SPREAD>'], axis = 1, inplace = True)
    currency.drop(['<DATE>'], axis = 1, inplace = True)
    currency.drop(['<TIME>'], axis = 1, inplace = True)
    
    #Creating the new dataframe---------------------------------------------------------------
    currency_formated = currency[start_date : end_date]
    
    #Calculating the 100th-standard deviation of prices close---------------------------------------
    currency_formated["100 Standard Deviation"] = currency_formated["Close"].rolling(100).std()
    
    #Adding the sma short and the sma long-----------------------------------------------------------
    sma_short = 5       
    sma_long  = 10
    currency_formated["sma_short"]  = currency_formated["Close"].rolling(sma_short).mean()
    currency_formated["sma_long"]   = currency_formated["Close"].rolling(sma_long).mean()
    
    #Taking off the NAN values-----------------------------------------------------------
    currency_formated = currency_formated.dropna(axis = 0) 
    
    #Calculating the number os contracts needed to normalize the volatility cross markets-----------
    currency_formated["Contracts"] = round(100 / (currency_formated["100 Standard Deviation"] * asset["Value PIP in USD"][a]))
    
    #Setting the variables of the system-----------------------------------------------------------
    equity      = pd.DataFrame(columns = ['#',
                                          'Enter Date',
                                          'End Date',
                                          'Enter Price',
                                          'End Price',
                                          'Numbers of Contracts',
                                          'Result',
                                          'Order'])
    
    
    count       = 1
    inTradeBuy  = False
    inTradeSell = False
    
    #Adding the rules of trade-----------------------------------------------------------
    for i in range(len(currency_formated)):       
        if inTradeBuy or inTradeSell :    
            #Rule to exit a sell signal------------------------------------------------------
            if inTradeBuy and (currency_formated["sma_short"][i] < currency_formated["sma_long"][i]):
                equity["End Date"][count]  = currency_formated["Date"][i]
                equity["End Price"][count] = currency_formated["Close"][i]
                inTradeBuy                 = False
                count                      = count + 1
            #Rule to exit a buy signal-------------------------------------------------------    
            if inTradeSell and (currency_formated["sma_short"][i] > currency_formated["sma_long"][i]):
                equity["End Date"][count]  = currency_formated["Date"][i]
                equity["End Price"][count] = currency_formated["Close"][i]
                inTradeSell                = False
                count                      = count + 1
        
        else:
            #Rule to enter in a buy side-------------------------------------------------------
            if (currency_formated["sma_short"][i] > currency_formated["sma_long"][i]):
                equity.loc[count, "Enter Date"]       = currency_formated["Date"][i]
                equity["Enter Price"][count]          = currency_formated["Close"][i]
                equity["Numbers of Contracts"][count] = currency_formated["Contracts"][i]
                equity["Order"][count]                = "Buy"
                equity["#"][count]                    = count
                inTradeBuy                            = True
                
            #Rule to enter in sell side-------------------------------------------------------   
            if (currency_formated["sma_short"][i] < currency_formated["sma_long"][i]): 
                equity.loc[count, "Enter Date"]       = currency_formated["Date"][i]
                equity["Enter Price"][count]          = currency_formated["Close"][i]
                equity["Numbers of Contracts"][count] = currency_formated["Contracts"][i]
                equity["Order"][count]                = "Sell"
                equity["#"][count]                    = count
                inTradeSell                           = True
            
    #Creating the table with results-----------------------------------------------------------
    
    equity["Enter Date"]   = pd.to_datetime(equity["Enter Date"], infer_datetime_format = True)
    equity["End Date"]     = pd.to_datetime(equity["End Date"], infer_datetime_format = True)
    equity["Enter Price"]  = equity["Enter Price"].astype(float)
    equity["End Price"]    = equity["End Price"].astype(float)
    equity["Result"]       = (equity["End Price"] - equity["Enter Price"]) * equity["Numbers of Contracts"]
    equity["Acum. Result"] = equity["Result"].cumsum()
    
    #Saving the results in a dedicated directory as a txt file---------------------------------
    adress1 = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\5M\\Currencies\\Moving Average CrossOver BackTesting\\"
    adress2 = "_result.txt"
    adress_final = adress1+asset["Currencies"][a]+adress2
    equity.to_csv(adress_final, index=False, sep = ';')