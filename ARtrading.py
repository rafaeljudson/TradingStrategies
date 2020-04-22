"""
Created on Wed Apr  1 01:53:43 2020

@author: Rafael Valle
"""
import Backtest
import Strategies

adress      = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\5M\\Currencies\\"
pair        = "DOL_5M"
destination = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\BackTest\Momentum\\"
decimal     = 0
volume      = 1000

test   = Backtest.formatDataFrameVol(Backtest.getDataFrame(adress, pair), decimal)

result = Strategies.strategyAR(pair, test, volume)

Backtest.savingResult(destination, pair, result)

Backtest.reportingResult(result)

Backtest.showingResult(result)
