# Made by Vigo Walker

from pocket_option_tools import pocketoption
from ta.trend import MACD, EMAIndicator
from ta.momentum import RSIIndicator
import time

ssid = (r'42["auth",{"session":"d4aai4ulkjnpdeoan08n1gmhgr","isDemo":1,"uid":84011929,"platform":2}]')
demo = True
api = pocketoption(ssid, demo)

last_trade = None  # Track the last trade type (either "call" or "put")

def calculate_fractals(high, low, window=3):
    bullish_fractals = []
    bearish_fractals = []
    
    for i in range(window, len(high)-window):
        # Bearish Fractal (High)
        if all(high[i] > high[j] for j in range(i-window, i)) and \
           all(high[i] > high[j] for j in range(i+1, i+window+1)):
            bearish_fractals.append(True)
        else:
            bearish_fractals.append(False)
            
        # Bullish Fractal (Low)
        if all(low[i] < low[j] for j in range(i-window, i)) and \
           all(low[i] < low[j] for j in range(i+1, i+window+1)):
            bullish_fractals.append(True)
        else:
            bullish_fractals.append(False)
            
    return bullish_fractals, bearish_fractals

while True:
    try:
        data = api.GetCandles("AUDCAD_otc", 60)
        print(len(data))
        # MACD calculation
        macd_indicator = MACD(data["close"], window_slow=26, window_fast=12, window_sign=9)
        macd_line = macd_indicator.macd()
        signal_line = macd_indicator.macd_signal()
        histogram = macd_indicator.macd_diff()

        # RSI calculation
        rsi = RSIIndicator(data["close"], window=14).rsi()
        
        # EMA calculation
        ema_25 = EMAIndicator(data["close"], window=25).ema_indicator()

        # Cálculo de fractales
        bullish_fractals, bearish_fractals = calculate_fractals(data["high"], data["low"])

        # Get the last values
        macd_val = macd_line.iloc[-1]
        signal_val = signal_line.iloc[-1]
        hist_val = histogram.iloc[-1]
        rsi_val = rsi.iloc[-1]
        ema_val = ema_25.iloc[-1]
        
        # Análisis de tendencia usando MACD y EMA
        trend_up = (histogram.iloc[-3:].mean() > 0 and 
                   data["close"].iloc[-1] > ema_val and 
                   rsi_val > 50)  # Tendencia alcista
        
        trend_down = (histogram.iloc[-3:].mean() < 0 and 
                     data["close"].iloc[-1] < ema_val and 
                     rsi_val < 50)  # Tendencia bajista

        # Condiciones de trading
        bullish_crossover = (macd_val > signal_val and 
                           trend_up and 
                           (len(bullish_fractals) > 0 and bullish_fractals[-1]))
        
        bearish_crossover = (macd_val < signal_val and 
                           trend_down and 
                           (len(bearish_fractals) > 0 and bearish_fractals[-1]))
        
        print(bullish_crossover, bearish_crossover )
        
        if bullish_crossover and last_trade != "call":
            print("Bullish crossover with trend - Placing a CALL order")
            print(f"RSI: {rsi_val:.2f} | MACD Hist: {hist_val:.5f}")
            api.Call(expiration=60, amount=1)
            last_trade = "call"

        elif bearish_crossover and last_trade != "put":
            print("Bearish crossover with trend - Placing a PUT order")
            print(f"RSI: {rsi_val:.2f} | MACD Hist: {hist_val:.5f}")
            api.Put(expiration=60, amount=1)
            last_trade = "put"
        else:
            print("No trade... Waiting for better conditions", end='\r')

        time.sleep(1)

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"An error occurred: {e}")
