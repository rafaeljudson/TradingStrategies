# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 01:53:43 2020

@author: Rafael Valle
"""
import Backtest
import Strategies

adress      = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\5M\\Currencies\\"
pair        = "DOL"
destination = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\BackTest\Momentum\\"
decimal     = 0
period      = 3660
multiplier  = 3

test   = Backtest.formatDataFrame(Backtest.getDataFrame(adress, pair), decimal)

result = Strategies.strategyMomentumII(pair, test, period, multiplier)

Backtest.savingResult(destination, pair, result)

Backtest.reportingResult(result)

Backtest.showingResult(result)
