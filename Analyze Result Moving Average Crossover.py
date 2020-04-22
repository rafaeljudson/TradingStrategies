# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:22:53 2020

@author: Rafael Valle

Description: Program to analyze the results of Moving Average Crossover program
"""

#Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#List of all currencies that we want to analyze the results of the moving average crossover strategy---------------------------------------------------
assets = {'Currencies':["CADCHF", "CADJPY", "CHFJPY", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPUSD", "USDBRL", "USDCAD", "USDCHF", "USDJPY"],
          'Value PIP in USD':[10.15, 8.99, 8.99, 6.90, 10.15, 11.55, 8.99, 10.00, 6.90, 10.15, 8.99, 10.00, 1.94, 6.90, 10.15, 8.99]}

asset = pd.DataFrame.from_dict(assets)

#Creating the dataframe to join all results
performance = pd.DataFrame(columns = ["Currency", "Date", "Result", "Order"])

#inde of dataframe performance counter
n = 1
#Reading all result and put in a single dataframe---------------------------------------------------------------
for i in range(len(asset)):    
    #Reading the csv result--------------------------------------------------------------------------------------------------------------------------------
    path1      = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\5M\\Currencies\\Moving Average CrossOver BackTesting\\"
    path2      = "_result.txt"
    path_total = path1+asset["Currencies"][i]+path2
    result = pd.read_csv(path_total, sep = ';')
    
    #Clean the data------------------------------------------------------------------------------------------------
    #result = result.set_index("#")
    result = result.dropna(axis = 0)                          
    
    
    
    
    for a in range(len(result)):
        performance.loc[n, "Date"] = result["End Date"][a]
        performance["Currency"][n] = asset["Currencies"][i]
        performance["Result"][n]   = result["Result"][a]*asset["Value PIP in USD"][i]
        performance["Order"][n]    = result["Order"][a]
        n = n + 1
#Showing the results    
performance.sort_values(by=['Date'], inplace = True, ascending = True)
performance = performance.set_index("Date")
print(performance.iloc[0:10])
print(performance.tail())
performance["Result"].cumsum().plot()

#Saving the results in txt file
performance.to_csv("C:\\Users\\rafae\\Desktop\\Dados de Mercado\\5M\\Currencies\\Moving Average CrossOver BackTesting\\Result_Final.txt", index=False, sep = ';')