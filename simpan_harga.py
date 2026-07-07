import os
import requests
import yfinance as yf
import pandas as pd

# Masukkan sebanyak mana kaunter yang anda mahu di sini
SYMBOLS = ['NVDA', 'AAPL', 'TSLA', 'AMD','DELL,'AVGO','ORCL','PLTR,'INTC','NVO','SPCX','WMT','BAC','NOW,'0166.KL'] 
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def get_indicators(df):
    # RSI (14)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs.iloc[-1]))
    
    # MACD (12, 26, 9)
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    
    # EMA 200
    ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    
    return rsi, macd.iloc[-1], signal.iloc[-1], ema200

def hantar_telegram(mesej):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': mesej, 'parse_mode': 'HTML'})

laporan = "🧠 <b>LAPORAN GENIUS BOT V2</b>\n"

for s in SYMBOLS:
    stock = yf.Ticker(s)
    hist = stock.history(period="250d") # Perlu data cukup untuk EMA 200
    harga = hist['Close'].iloc[-1]
    rsi, macd, signal, ema200 = get_indicators(hist)
    
    # Logik Keputusan "Genius"
    status = "HOLD ⚪"
    if rsi > 70 or (macd > signal and harga < ema200):
        status = "💰 <b>SELL (Profit Taking)</b>"
    elif rsi < 30 and macd < signal:
        status = "🛒 <b>BUY (Potential Bottom)</b>"
    elif harga > ema200 and macd > signal:
        status = "🚀 <b>STRONG BUY/HOLD (Bullish)</b>"
            
    laporan += f"\n<b>{s}</b>: ${harga:.2f}\nRSI: {rsi:.1f} | MACD: {'+' if macd>signal else '-'}\nEMA200: ${ema200:.2f}\nStatus: {status}\n"

hantar_telegram(laporan)
