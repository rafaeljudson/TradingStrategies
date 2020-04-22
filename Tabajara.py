"""
Created on Wed Apr  1 01:53:43 2020

@author: Rafael Valle
"""
import Backtest
import Strategies

adress      = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\5M\\Indexes\\"
pair        = "Ibov_5M"
destination = "C:\\Users\\rafae\\Desktop\\Dados de Mercado\\BackTest\Momentum\\"
decimal     = 0
ma_short    = 8
ma_long     = 20
volume      = 1000
test   = Backtest.formatDataFrameVol(Backtest.getDataFrame(adress, pair), decimal)

result = Strategies.strategyTabajara(pair, test, ma_short, ma_long, volume)

Backtest.savingResult(destination, pair, result)

Backtest.reportingResult(result)

Backtest.showingResult(result)
