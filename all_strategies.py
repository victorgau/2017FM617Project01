import numpy as np
import pandas as pd
import talib
from talib import MA_Type

# 這是我們的策略的部分
# 主要只是要算出進出的訊號 signals 跟何時持有部位 positions
# 底下是一個突破系統的範例

def Breakout_strategy(df):
    # Donchian Channel
    df['20d_high'] = np.round(pd.Series.rolling(df['Close'], window=20).max(), 2)
    df['10d_low'] = np.round(pd.Series.rolling(df['Close'], window=10).min(), 2)

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['Close'][t] > df['20d_high'][t-1]:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['Close'][t] < df['10d_low'][t-1]:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def RSI_7030_strategy(df):
    df['RSI'] = talib.RSI(df['Close'].values)

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['RSI'][t-1] < 30:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['RSI'][t-1] > 70:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def RSI_8020_strategy(df):
    """
    RSI < 20: buy
    RSI > 80: sell
    """
    df['RSI'] = talib.RSI(df['Close'].values)

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['RSI'][t-1] < 20:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['RSI'][t-1] > 80:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def BBands_strategy(df):
    df['UBB'], df['MBB'], df['LBB'] = talib.BBANDS(df['Close'].values, matype=MA_Type.T3)

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['Close'][t] < df['LBB'][t-1]:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['Close'][t] > df['UBB'][t-1]:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def Team1_strategy(df):
    close=pd.DataFrame(df["Close"])
    short_win = 12    # 短期EMA平滑天数
    long_win  = 26    # 長期EMA平滑天数
    macd_win  = 20    # DEA線平滑天数
    macd_tmp  =  talib.MACD( df['Close'].values,fastperiod = short_win ,slowperiod = long_win ,signalperiod = macd_win )
    df['DIF'] =macd_tmp [ 0 ]
    df['DEA'] =macd_tmp [ 1 ]
    df['MACD']=macd_tmp [ 2 ]
    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['DIF'][t] > 0 and df['DEA'][t] >0 and df['DIF'][t] > df['DEA'][t] and df['DIF'][t-1]<df['DEA'][t-1]:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['DIF'][t] < 0 and df['DEA'][t] < 0 and df['DIF'][t] < df['DEA'][t] and df['DIF'][t-1]>df['DEA'][t-1]:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def Team3_strategy(df):
    """
    主要使用BBand + 5MA策略，
    中軌為20ma，上下軌為正負1.5sd
    # 若5MA開始向上突破下軌，低檔買進
    # 若收盤價向下跌破中軌，獲利了結趕快落跑
    """

    df['5ma'] = pd.Series.rolling(df['Close'], window=5).mean()
    # bbands策略,N=20
    df['20ma'] = pd.Series.rolling(df['Close'], window=20).mean()
    df['SD'] = pd.Series.rolling(df['Close'], window=20).std()
    # 上軌=20ma+1.5sd ,中軌=20ma, 下軌=20ma-1.5sd
    df['upbbands'] = df['20ma']+1.5*df['SD']
    df['midbbands']=df['20ma']
    df['lowbbands'] = df['20ma']-1.5*df['SD']

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if  (df['5ma'][t] > df['lowbbands'][t-1]):
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif  (df['Close'][t] < df['midbbands'][t-1]):
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df
