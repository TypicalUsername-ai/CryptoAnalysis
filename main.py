import coinGecko_API as api
import coin_analysis as analysis
import pandas as pd
import plotly.graph_objects as go
import datetime

session = api.getApiConnection()
coins = api.getSupportedCoins(session)
fiat = api.getSupportedFiat(session)
portfolio = analysis.getPortfolio()
watchlist = analysis.getWatchlist()

def checkPortfolio():
    print("\n checking portfolio...")
    for entry in portfolio:
        b_price = portfolio[entry]["avg-price"]
        amt = portfolio[entry]["amount"]
        n_price = api.getTetherPrice(session, entry)
        print(f"{amt} ${entry}: {b_price} -> {n_price} \n =>> {amt * b_price} -> {amt * n_price} ({(amt * n_price) - (amt * b_price)})")

def proposeInvestments(limit=30):
    analysis.updateToplist(session)
    proposals = pd.DataFrame(columns=["id", "time", "signal"])
    entries = []
    fullList = watchlist['tradeable']
    for entry in fullList:
        print(f"analyzing entry: {entry}")
        n_frame = api.getCandlestick(session, entry, 30)
        f_frame = analysis.getBTrends(n_frame,4)
        x = analysis.bTrendAnalysis(f_frame,entry)
        entries.append(entry)
        proposals = proposals.append(x,ignore_index=True)

    tMtwo = datetime.datetime.now() - datetime.timedelta(limit)
    daysBound = proposals[proposals['time'] >= tMtwo]
    analysis.savePredictions(daysBound)
    return daysBound


def displayCharts():
    pass

def checkWatchlist():
    print("\n checking watchlist \n")
    print("coins currently analyzed under TRADEABLE: \n")
    for entry in watchlist["tradeable"]:
        n_price = api.getTetherPrice(session, entry)
        print(f"\nentry: {entry}, current price {n_price}")
        n_frame = api.getCandlestick(session, entry, 30)
        t_frame = analysis.getBTrends(n_frame, 5)
        analysis.bTrendAnalysis(t_frame,entry)
        
        fig = analysis.candleStick(n_frame)
        fig.write_html(f"graphs/{entry}.html")

if __name__ == "__main__":
    #checkPortfolio()
    #checkWatchlist()
    print(proposeInvestments(15))
    
    # pFrame = api.getCandlestick(session, "bitcoin", 30)
    # tFrame = analysis.getBTrends(pFrame, 5)
    # analysis.bTrendAnalysis(tFrame)

    # how to nicely aggregate data -> classify candlesticks as bullish / bearish
    # then determine if any of the candlesticks are currently in the bearish pattern so can look for reversals
    # if any reversals are possible then go through each candlestick set to classify possible reversal patterns
    # -> probably like last 3 as we dont wanna predict the past
    # then we can write predictions to some points
    # then we can feed the predictions and found patterns and then results into an AI model in tensorflow
    # -> later the model can be used to also predict the price behavious based on previous models
    # + a simpler model can be programmed to help determine the trends :>>

    