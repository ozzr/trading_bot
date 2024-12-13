import pandas as pd
import talib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import ta

class FeatureProcessor:
    def __init__(self):
       pass

    @staticmethod
    def add_bar_features(df):
        df['bar_hc'] = df["high"] - df["close"]
        df['bar_ho'] = df["high"] - df["open"]
        df['bar_hl'] = df["high"] - df["low"]
        df['bar_cl'] = df["close"] - df["low"]
        df['bar_ol'] = df["open"] - df["low"]
        df['bar_co'] = df["close"] - df["open"]
        df['bar_mov'] = df['close'] - df['close'].shift(1)
        return df

    @staticmethod
    def add_mv_avg_features(df):
        df['sma5'] = talib.SMA(df["close"], 5)
        df['sma20'] = talib.SMA(df["close"], 20)
        df['sma120'] = talib.SMA(df["close"], 120)
        df['ema12'] = talib.EMA(df["close"], 12)
        df['ema26'] = talib.EMA(df["close"], 26)
        return df

    @staticmethod
    def add_adj_features(df):
        df['adj_open'] = df['open'] / df["close"]
        df['adj_high'] = df['high'] / df["close"]
        df['adj_low'] = df['low'] / df["close"]
        df['adj_close'] = df['close'] / df["close"]
        return df

    @staticmethod
    def add_ta_features(df):
        upper, middle, lower = talib.BBANDS(df["close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        df['dn'] = lower
        df['mavg'] = middle
        df['up'] = upper
        df['pctB'] = (df["close"] - df.dn) / (df.up - df.dn)
        df['rsi14'] = talib.RSI(df["close"], 14)
        df['macd'], df['signal'], df['macdhist'] = talib.MACD(df["close"], 12, 26, 9)
        df['adx'] = talib.ADX(df["high"], df["low"], df["close"], timeperiod=14)
        df['cci'] = talib.CCI(df["high"], df["low"], df["close"], timeperiod=14)
        df['plus_di'] = talib.PLUS_DI(df["high"], df["low"], df["close"], timeperiod=14)
        df['lower_bound'] = df['open'] - df['low'] + 1
        df['atr'] = talib.ATR(df["high"], df["low"], df["close"], timeperiod=14)
        
        # Oscilador Estocástico
        df['stoch_k'] = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close']).stoch()
        df['stoch_d'] = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close']).stoch_signal()

        # TRIX
        df['trix'] = talib.TRIX(df["close"], timeperiod=5)
        df['trix_signal'] = talib.SMA(df['trix'], timeperiod=3)
        df['trix_hist'] = df['trix'] - df['trix_signal']
        
        periods = {
            'short_term': 5,
            'medium_term': 15,
            'long_term': 30,
            'very_long_term': 60
        }
        
        for key, period in periods.items():
            df[f'donchian_high_{key}'] = df['high'].rolling(window=period).max()
            df[f'donchian_low_{key}'] = df['low'].rolling(window=period).min()
        # ## MFI
        # df['mfi14'] = ta.volume.money_flow_index(df, 14)
        
        return df
    @staticmethod
    def add_time_features(df):
        timestamp_s = df.index.map(pd.Timestamp.timestamp)
        day = 24*60*60
        week = day * 7
        year = (365.2425) * day
        df['daysin']  = np.sin(timestamp_s * (2 * np.pi / day)) 
        df['daycos']  = np.cos(timestamp_s * (2 * np.pi / day)) 
        df['weeksin'] = np.sin(timestamp_s * (2 * np.pi / week)) 
        df['weekcos'] = np.cos(timestamp_s * (2 * np.pi / week)) 
        
        
        # df['delta'] = df['high'] - df['low']
        return df
    
    @staticmethod
    def add_stationary_features(df):
        df['open_diff'] = df['open'].diff()
        df['high_diff'] = df['high'].diff()
        df['low_diff'] = df['low'].diff()
        df['close_diff'] = df['close'].diff()
        return df