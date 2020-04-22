# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:57:32 2020

@author: Rafael Valle

@Description: 
"""

import pandas as pd

def tableResult():
    
    print("Creating the Table of Results of the Strategy")
    
    result = pd.DataFrame(columns = ['Currency',
                                     'Order',
                                     'Enter Date',
                                     'End Date',
                                     'Numbers of Contracts',
                                     'Enter Price',
                                     'End Price',
                                     'Result',
                                     'Result U$D'])
    
    return result