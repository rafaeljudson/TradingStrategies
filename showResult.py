# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""

import matplotlib.pyplot as plt


def showResult(result):
    
    print("Showing the Results")
    
    result["Result U$D"].cumsum().plot()
    
    return result