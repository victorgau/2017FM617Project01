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

def JuianJuian4715_strategy(df):
    has_position = False
    df['signals'] = 0
    """
    ##strategy:以20MA為中心，上下各2個標準差為範圍的一個軌道操作方式。
    ##買進訊號:
    #1.價格由下向上 穿越下軌線時，是買進訊號
    #2.價格由下向上 穿越中間線時，股價可能加速向上，是加碼買進訊號
    #3.價格在中間線與上軌線之間波動時，為多頭市場，可作多
    """
    ave = pd.Series.rolling(df['Close'], window=20).mean() 
    std = pd.Series.rolling(df['Close'], window=20).std()
    df['ave']= pd.Series.rolling(df['Close'], window=20).mean()
    df['upper'] = ave + 2*std
    df['lower'] = ave -2*std

    for t in range(2, df['signals'].size):
        if df['upper'][t] > df['ave'][t-1]:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['lower'][t] < df['ave'][t-1]:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False



    df['positions'] = df['signals'].cumsum().shift()
    return df
