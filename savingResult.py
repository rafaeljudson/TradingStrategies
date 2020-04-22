# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""
def savingResult(result, pair, adress):
    
    print("Saving the Results in a txt file")
    
    adress2 = "_result.txt"
    adress_final = adress + pair + adress2
    result.to_csv(adress_final, index=False, sep = ';')
    
    return