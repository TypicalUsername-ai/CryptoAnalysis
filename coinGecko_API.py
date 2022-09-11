import requests
import json
import crypto_coin as coin
import pandas as pd
import datetime

api = "https://api.coingecko.com/api/v3"
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin"

def getApiConnection():
    s = requests.Session()

    test_res = s.get(api+"/ping")
    if test_res.status_code == 200:
        print(test_res.text)
        print("connection online, starting session...")
        return s
    else:
        print("failure to establish connection")
        raise ConnectionError(f"session start response code other than 200 <{test_res.status_code}>")

def getSupportedCoins(session):
    res = session.get(api+"/coins/list")
    res_json = json.loads(res.text)
    print(f"\n currently there are {len(res_json)} coins supported")
    c_list = {}
    for coin_json in res_json:
        c_obj = coin.crypto(coin_json)
        c_list.update({c_obj.id:c_obj})

    return c_list

def getSupportedFiat(session):
    res = session.get(api+"/simple/supported_vs_currencies")
    res_json = json.loads(res.text)
    print(f"\n currently there are {len(res_json)} fiat currencies supported")
    return res_json

def getTetherPrice(session, coin_id):
    res = session.get(api+f"/simple/price?ids={coin_id}&vs_currencies=usd")
    if res.status_code == 200:
        json_res = json.loads(res.text)
        #print(json_res[coin_id]["usd"])
        return json_res[coin_id]["usd"]
    else:
        raise ConnectionRefusedError("no connection (status code != 200)")

def getPriceAtDate(session, coin_id, start, end):
    res = session.get(api+f"/coins/{coin_id}/market_chart/range?vs_currency=usd&from={start}&to={end}")
    if res.status_code == 200:
        json_res = json.loads(res.text)
        #get the valueee
        
    else:
        raise ConnectionRefusedError("no connection (status code != 200)")

def getCandlestick(session, coin_id, days) -> pd.DataFrame:
    res = session.get(api+f"/coins/{coin_id}/ohlc?vs_currency=usd&days={days}")
    if res.status_code == 200:
        json_res = json.loads(res.text)
        for tFrame in json_res:
            z = datetime.datetime.fromtimestamp(tFrame[0] / 1000)#.strftime('%Y-%m-%d %H:%M:%S')
            tFrame[0] = z
        dataFr = pd.DataFrame(json_res, columns=["time", "open", "high", "low", "close"])
        return dataFr

def getTrending(session):
    trending_coin = []
    res = session.get(api+f"/search/trending")
    if res.status_code == 200:
        json_res = json.loads(res.text)
        for n_coin in json_res['coins']:
            trending_coin.append(coin.crypto(n_coin['item']))
    return trending_coin

if __name__ == "__main__":
    sesh = getApiConnection()
    coinList = getSupportedCoins(sesh)
    print(coinList["tether"])
    fiatList = getSupportedFiat(sesh)
    print(getTetherPrice(sesh,"tether"))

    x = getCandlestick(sesh, "bitcoin", 1)
    
    print(getTrending(sesh))