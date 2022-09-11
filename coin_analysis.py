import datetime
import json
import pandas as pd
import plotly.graph_objects as go
import coinGecko_API as api
from trade_patterns import patterns as patterns

plistPath = "portfolio.json"
wlistPath = "watchlist.json"
predPath = "predictions.json"

def updateToplist(session):
    pf = getWatchlist()
    tops_l = []
    tops = api.getTrending(session)
    for entry in tops:
        tops_l.append(entry.id)
    pf['top'] = tops_l
    with open(wlistPath, 'w') as file:
        file.write(json.dumps(pf, indent=1))
    return True

def savePredictions(frame):
    current = frame.copy()
    previous = pd.read_json(predPath, convert_dates=True)
    target = []
    for index, row in frame.iterrows():
        #print(row)
        target.append(row['time'] + datetime.timedelta(0.5))
    
    current['target'] = target
    #print(current.to_json(indent=1))
    previous = previous.append(current, ignore_index=True, verify_integrity=True)
    previous.drop_duplicates(inplace=True, keep="first", subset=['time', 'id']) #.drop_duplicates(inplace=True,keep="first",subset=["sekwencja"])
    file = open(predPath, 'w')
    file.write(previous.to_json(indent=1))
    return True

def checkPredictions(session):
    now = datetime.datetime.now()
    print(f"<{now}>: CHECKING PREVIOUS PREDICTIONS <---------------------------------!!!")
    preds = pd.read_json(predPath, convert_dates=True)
    for index, row in preds.iterrows():
        target = datetime.datetime.fromtimestamp(row['target'] / 1000)
        time = datetime.datetime.fromtimestamp(row['time'] / 1000)
        if (now > target):
            print(f"<{now}>: {row['id']} @ [{time} >> {target}] calculating...")
            # code for calculationg whetrher the prediction was true...
            preds.drop(index=index, inplace=True)
    print(preds)
    file = open(predPath, 'w')
    file.write(preds.to_json(indent=1))

    return preds


def getPortfolio():
    with open(plistPath, 'r') as file:
        wlist = json.loads(file.read())

    #print(wlist)
    return wlist

def getWatchlist():
    with open(wlistPath, 'r') as file:
        wlist = json.loads(file.read())

    #print(wlist)
    return wlist

def candleStick(frame):
    fig = go.Figure(data=[go.Candlestick(
        x = frame['time'], 
        open = frame['open'], 
        high = frame['high'], 
        low = frame['low'], 
        close  = frame['close'])])
    return fig

def getBTrends(frame, sensitivity):
    trend_s = []
    change_s = []
    cont_s = []
    for index, row in frame.iterrows():
        change = ((row['close'] - row['open']) / row['open']) * 100
        #print(f"{index} :  {row['open']} => {row['close']}", end=' ')
        if row['open'] < row['close'] and change >= (sensitivity / 10):
            trend = 'bullish'
            
        elif row['open'] > row['close'] and change <= -(sensitivity/10):
            trend = 'bearish'
        else:
            trend = 'stale'

       # print(trend, end=' ')
        num = 0
        if index != 0:
            if trend_s[index-1] != trend:
                pass
            else:
                num = cont_s[index-1] + 1

        trend_s.append(trend)
        change_s.append(change)
        cont_s.append(num)

    frame['trend'] = trend_s
    frame['% change'] = change_s
    frame['cont cycles'] = cont_s
    #print(frame)

    return frame

def bTrendAnalysis(BtrendFrame, entry):

    invWindows = []

    possibleRev = False
    for index, row in BtrendFrame.iterrows():

        if row['trend'] == 'bullish' and possibleRev:
            #print(f"<{row['time']}>: POSSIBLE REVERSAL <--------------------------------!!!")
            hh = patterns.hammer(BtrendFrame, index)
            if hh:
                print(f"<{row['time']}> ==>")
                print(f"<{BtrendFrame.iloc[hh]['time']}>: reversal by hammer <--------------------------------!!!")
                invWindows.append([entry, row['time'], "hammer"])

            ih = patterns.i_hammer(BtrendFrame, index)
            if ih:
                print(f"<{row['time']}> ==>")
                print(f"<{BtrendFrame.iloc[ih]['time']}>: reversal by inverse hammer <--------------------------------!!!")
                invWindows.append([entry, row['time'], "inverse hammer"])

            en = patterns.engulf(BtrendFrame, index)
            if en:
                print(f"<{row['time']}> ==>")
                print(f"<{BtrendFrame.iloc[en]['time']}>: reversal by engulf <--------------------------------!!!")
                invWindows.append([entry, row['time'], "engulf"])

            pl = patterns.piercing_line(BtrendFrame, index)
            if pl:
                print(f"<{row['time']}> ==>")
                print(f"<{BtrendFrame.iloc[pl]['time']}>: reversal by piercing line <--------------------------------!!!")
                invWindows.append([entry, row['time'], "piercing line"])

            ts = patterns.three_soldiers(BtrendFrame, index)
            if ts:
                print(f"<{row['time']}> ==>")
                print(f"<{BtrendFrame.iloc[ts]['time']}>: reversal by three soldiers! <--------------------------------!!!")
                invWindows.append([entry, row['time'], "three soldiers"])
                
            
            possibleRev = False


        if row['cont cycles'] >= 3 and row['trend'] == 'bearish':
                #print(f"<{row['time']}>: {row['cont cycles']} {row['trend']} at {row['time']}")
                possibleRev = True
    
    return pd.DataFrame(data=invWindows, columns=["id","time", "signal"])


if __name__ == "__main__":
    sesh = api.getApiConnection()

    updateToplist(sesh)

    checkPredictions(sesh)
