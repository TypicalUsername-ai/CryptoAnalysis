class patterns:
    def hammer(frame, index):
        data = frame.iloc[index]
        #print(data)
        tail = data['open'] - data['low']
        body = data['close'] - data['open']
        top = data['high'] - data['close']
        #print(f"<{data['time']}>: tail: {tail}, body: {body}, top: {top} ")
        if tail * 1.5 >= body and top == 0:
            return index
        else:
            return False

    def i_hammer(frame, index):
        data = frame.iloc[index]
        #print(data)
        tail = data['open'] - data['low']
        body = data['close'] - data['open']
        top = data['high'] - data['close']
        #print(f"<{data['time']}>: tail: {tail}, body: {body}, top: {top} ")
        if top * 1.5 >= body and tail == 0:
            return index
        else:
            return False

    def engulf(frame, index):
        prev = frame.iloc[index-1]
        data = frame.iloc[index]
        if data['open'] <= prev['close'] and data['close'] > prev['open']:
            #print(data, prev)
            return index
        else:
            return False

    def piercing_line(frame, index):
        prev = frame.iloc[index-1]
        data = frame.iloc[index]
        if data['open'] < prev['close'] and data['close'] >= prev['open'] * 0.52:
            return index
        else:
            return False

    def three_soldiers(frame, index) -> bool:
        for trend in frame.iloc[index:index+3]['trend'].array:
            if trend != 'bullish':
                return False
        return index
