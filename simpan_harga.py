import os
import requests
import yfinance as yf
import pandas as pd

SYMBOLS = ['NVDA', 'AAPL']
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def get_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs.iloc[-1]))

def hantar_telegram(mesej):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': mesej, 'parse_mode': 'HTML'})

laporan = "🤖 <b>LAPORAN ANALISIS AUTOMATIK</b>\n"

for s in SYMBOLS:
    stock = yf.Ticker(s)
    hist = stock.history(period="60d")
    harga = hist['Close'].iloc[-1]
    ma50 = hist['Close'].rolling(window=50).mean().iloc[-1]
    rsi = get_rsi(hist)
    
    # Logik Keputusan Automatik
    if rsi > 70:
        status = "💰 <b>SELL (Overbought)</b>"
    elif rsi < 30:
        status = "🛒 <b>BUY (Oversold)</b>"
    elif harga > ma50:
        status = "🟢 <b>HOLD (Bullish Trend)</b>"
    else:
        status = "🔴 <b>HOLD/WATCH (Bearish Trend)</b>"
            
    laporan += f"\n<b>{s}</b>\nHarga: ${harga:.2f}\nRSI: {rsi:.2f}\nStatus: {status}\n"

hantar_telegram(laporan)
